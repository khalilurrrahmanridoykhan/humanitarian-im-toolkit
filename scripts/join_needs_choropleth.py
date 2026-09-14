"""Joins the synthetic site-assessment data to official P-coded administrative
boundaries and produces a needs-severity choropleth.

The join key is the official P-code (adm3_pcode), never the upazila name —
`data/upazila_pcode_crosswalk.csv` documents two real name mismatches between
our synthetic data's slugs and the official HDX COD-AB names (e.g. "ukhiya"
vs. official "Ukhia"), which is exactly the failure mode a name-based join
would hit silently.

Boundary source: HDX "Bangladesh - Subnational Administrative Boundaries"
(cod-ab-bgd, BBS/ITOS via UNOCHA ROAP), filtered to the 6 upazilas this
synthetic dataset covers -> data/cod/bgd_admin3_coxsbazar_subset.geojson.

Run: python3 scripts/join_needs_choropleth.py
Outputs:
  data/needs_choropleth_coxsbazar.geojson  (joined, QGIS-ready)
  data/needs_choropleth_coxsbazar.png      (static render)
  data/needs_choropleth.qml                (QGIS graduated-symbology style)
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

SITES_CSV = "data/synthetic_site_assessments.csv"
CROSSWALK_CSV = "data/upazila_pcode_crosswalk.csv"
BOUNDARY_GEOJSON = "data/cod/bgd_admin3_coxsbazar_subset.geojson"

OUT_GEOJSON = "data/needs_choropleth_coxsbazar.geojson"
OUT_PNG = "data/needs_choropleth_coxsbazar.png"
OUT_QML = "data/needs_choropleth.qml"

DAMAGE_MIDPOINT = {
    "": 0, "none": 0, "low_1_25": 13, "moderate_26_50": 38,
    "high_51_75": 63, "severe_76_100": 88,
}
WATER_FUNCTIONALITY_SEVERITY = {
    "functional": 0, "partially_functional": 50, "non_functional": 100,
}


def compute_needs_score(sites: pd.DataFrame) -> pd.DataFrame:
    sites = sites.copy()
    sites["shelter_severity"] = sites["shelter/shelter_damage_pct"].fillna("").map(DAMAGE_MIDPOINT).fillna(0)
    sites["water_severity"] = sites["wash/water_functionality"].map(WATER_FUNCTIONALITY_SEVERITY).fillna(0)
    sites["protection_count"] = sites["protection/protection_concerns"].fillna("").apply(
        lambda v: len(v.split()) if v else 0
    )
    sites["health_priority_flag"] = (sites["health/health_priority_need"] == "yes").astype(int) * 100

    grouped = sites.groupby("location/upazila").agg(
        n_sites=("site_id", "count"),
        avg_shelter_severity=("shelter_severity", "mean"),
        avg_water_severity=("water_severity", "mean"),
        avg_protection_count=("protection_count", "mean"),
        pct_health_priority=("health_priority_flag", "mean"),
    ).reset_index()

    # protection_count typically ranges 0-2 in this instrument; scale to 0-100
    grouped["protection_severity"] = (grouped["avg_protection_count"] / 2.0 * 100).clip(upper=100)

    grouped["needs_score"] = (
        0.30 * grouped["avg_shelter_severity"]
        + 0.25 * grouped["avg_water_severity"]
        + 0.20 * grouped["pct_health_priority"]
        + 0.25 * grouped["protection_severity"]
    ).round(1)

    return grouped


def main():
    sites = pd.read_csv(SITES_CSV)
    crosswalk = pd.read_csv(CROSSWALK_CSV)
    needs = compute_needs_score(sites)

    needs = needs.merge(
        crosswalk, left_on="location/upazila", right_on="synthetic_upazila_slug", how="left"
    )
    missing = needs[needs["official_adm3_pcode"].isna()]
    if not missing.empty:
        raise SystemExit(f"Upazila slugs with no P-code crosswalk entry: {missing['location/upazila'].tolist()}")

    boundaries = gpd.read_file(BOUNDARY_GEOJSON)
    joined = boundaries.merge(
        needs, left_on="adm3_pcode", right_on="official_adm3_pcode", how="left"
    )
    unmatched_boundaries = joined[joined["needs_score"].isna()]
    if not unmatched_boundaries.empty:
        names = unmatched_boundaries["adm3_name"].tolist()
        print(f"Note: boundary polygons with no matching site data (expected if not all 6 upazilas were sampled): {names}")

    joined.to_file(OUT_GEOJSON, driver="GeoJSON")
    print(f"wrote {OUT_GEOJSON} ({len(joined)} polygons, joined on adm3_pcode)")

    fig, ax = plt.subplots(figsize=(8, 8.5))
    joined.plot(
        column="needs_score", cmap="OrRd", linewidth=0.6, edgecolor="black",
        legend=True, ax=ax, missing_kwds={"color": "lightgrey", "label": "No data"},
    )
    for _, row in joined.iterrows():
        if pd.notna(row["needs_score"]):
            ax.annotate(row["adm3_name"], xy=row.geometry.centroid.coords[0], ha="center", fontsize=7)
    ax.set_title(
        "Synthetic needs-severity score by upazila (Cox's Bazar area)\n"
        "Joined on official P-codes (HDX COD-AB) -- fabricated demonstration data",
        fontsize=10, wrap=True,
    )
    ax.set_axis_off()
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(OUT_PNG, dpi=150)
    print(f"wrote {OUT_PNG}")

    write_qml(OUT_QML)
    print(f"wrote {OUT_QML}")


def write_qml(path: str):
    # QGIS graduated-symbology style for the `needs_score` field, equal-
    # interval 5-class OrRd ramp matching the PNG render above. Each
    # SimpleFill layer's <Option> wrapper MUST carry type="Map" -- without
    # it QGIS can't read `color` as a map entry and silently falls back to
    # a default fill instead of erroring, which is exactly what happened
    # the first time this file shipped (caught by actually opening it in
    # QGIS, not by any automated check -- xls2xform-style tools don't
    # validate .qml).
    colors = [
        "255,255,204,255", "254,217,142,255", "254,153,41,255",
        "217,95,14,255", "153,52,4,255",
    ]
    ranges = [
        ("0 - 20 (low)", 0, 20), ("20 - 40", 20, 40),
        ("40 - 60 (moderate)", 40, 60), ("60 - 80", 60, 80),
        ("80 - 100 (severe)", 80, 100),
    ]

    range_xml = "\n".join(
        f'      <range label="{label}" lower="{lo}" upper="{hi}" render="true" symbol="{i}"/>'
        for i, (label, lo, hi) in enumerate(ranges)
    )
    symbol_xml = "\n".join(
        f"""      <symbol type="fill" name="{i}" alpha="1" clip_to_extent="1" force_rhr="0">
        <layer class="SimpleFill" locked="0" pass="0" enabled="1">
          <Option type="Map">
            <Option type="QString" name="color" value="{color}"/>
            <Option type="QString" name="outline_color" value="35,35,35,255"/>
            <Option type="QString" name="outline_style" value="solid"/>
            <Option type="QString" name="outline_width" value="0.26"/>
            <Option type="QString" name="outline_width_unit" value="MM"/>
            <Option type="QString" name="style" value="solid"/>
          </Option>
        </layer>
      </symbol>"""
        for i, color in enumerate(colors)
    )

    qml = f"""<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.34" styleCategories="Symbology">
  <renderer-v2 type="graduatedSymbol" attr="needs_score" graduatedMethod="GraduatedColor">
    <ranges>
{range_xml}
    </ranges>
    <symbols>
{symbol_xml}
    </symbols>
  </renderer-v2>
</qgis>
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(qml)


if __name__ == "__main__":
    main()
