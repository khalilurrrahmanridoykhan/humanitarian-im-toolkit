"""Phase R6: joins this toolkit's needs-severity output to a hazard/risk
layer from geohealth-risk-mapping (github.com/khalilurrrahmanridoykhan/
geohealth-risk-mapping), on official P-code -- a documented, file-based join
path with no code coupling: neither repo imports the other.

Honest current-state check (done before writing this, not assumed):
geohealth-risk-mapping's own PLAN.md places its ward-level **risk score**
at Phase H10, and as of this writing that project has completed through H7
-- H10 doesn't exist yet. Its one real zonal-stats output so far
(data/processed/dhaka_smoke_tile_zonal_stats.csv) also keys admin units by
plain district *name* ("Dhaka", "Gazipur", "Narayanganj"), not by P-code.

So there is no real file to join to today. What this script does instead:
implements and demonstrates the join contract against this repo's own real
R3 output (data/needs_choropleth_coxsbazar.geojson, P-code-keyed) and a
clearly-labeled placeholder hazard table
(data/geohealth_integration/mock_hazard_placeholder.csv) matching the
schema geohealth-risk-mapping's H10 output should use. See
docs/geohealth-integration.md for the full contract and the recommendation
that H10 adopt P-codes as its join key -- the same ukhiya-vs-Ukhia lesson
Phase R3 already hit here.

Run: python3 scripts/join_hazard_needs_overlay.py
Outputs:
  data/geohealth_integration/combined_priority_coxsbazar.geojson
  data/geohealth_integration/combined_priority_coxsbazar.png
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

NEEDS_GEOJSON = "data/needs_choropleth_coxsbazar.geojson"
HAZARD_CSV = "data/geohealth_integration/mock_hazard_placeholder.csv"

OUT_GEOJSON = "data/geohealth_integration/combined_priority_coxsbazar.geojson"
OUT_PNG = "data/geohealth_integration/combined_priority_coxsbazar.png"

# Equal weight by default -- a real deployment would tune this against
# what the hazard score and needs score actually represent.
NEEDS_WEIGHT = 0.5
HAZARD_WEIGHT = 0.5


def main():
    needs = gpd.read_file(NEEDS_GEOJSON)
    hazard = pd.read_csv(HAZARD_CSV)

    if (hazard["source"] == "SYNTHETIC_PLACEHOLDER").any() or hazard["source"].str.startswith("SYNTHETIC_PLACEHOLDER").any():
        print(
            "NOTE: hazard_score below is a SYNTHETIC PLACEHOLDER, not a real "
            "geohealth-risk-mapping output -- that project has not reached its "
            "risk-scoring phase (H10) for this area yet. This run proves the "
            "join mechanism, not a real combined risk figure. See "
            "docs/geohealth-integration.md."
        )

    joined = needs.merge(hazard, left_on="adm3_pcode", right_on="adm3_pcode", how="left")
    unmatched = joined[joined["hazard_score"].isna()]
    if not unmatched.empty:
        raise SystemExit(f"P-codes with no hazard match: {unmatched['adm3_name_x'].tolist()}")

    joined["combined_priority_score"] = (
        NEEDS_WEIGHT * joined["needs_score"] + HAZARD_WEIGHT * joined["hazard_score"]
    ).round(1)

    joined.to_file(OUT_GEOJSON, driver="GeoJSON")
    print(f"wrote {OUT_GEOJSON} ({len(joined)} polygons, joined on adm3_pcode)")

    fig, axes = plt.subplots(1, 3, figsize=(15, 6))
    for ax, col, title, cmap in [
        (axes[0], "needs_score", "Needs score\n(Phase R3, real synthetic-survey aggregate)", "Blues"),
        (axes[1], "hazard_score", "Hazard score\n(PLACEHOLDER -- geohealth-risk-mapping H10 not built yet)", "Oranges"),
        (axes[2], "combined_priority_score", "Combined priority score\n(demonstration only)", "OrRd"),
    ]:
        joined.plot(column=col, cmap=cmap, edgecolor="black", linewidth=0.5, legend=True, ax=ax)
        ax.set_title(title, fontsize=9)
        ax.set_axis_off()

    fig.suptitle(
        "Phase R6: needs + hazard overlay demonstration (Cox's Bazar area) -- "
        "hazard layer is a placeholder, see docs/geohealth-integration.md",
        fontsize=10,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(OUT_PNG, dpi=150)
    print(f"wrote {OUT_PNG}")


if __name__ == "__main__":
    main()
