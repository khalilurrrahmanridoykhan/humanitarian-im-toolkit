"""Rapid-mapping task grid + QA validation for a real OSM building/road extract.

Scope note (read this before assuming what this script claims): manual
imagery tracing in JOSM/the iD editor is a hands-on GUI skill that isn't
something a script can honestly perform or claim credit for -- same as
KoboToolbox/ArcGIS Online, that stays with whoever actually does it. What
*is* scriptable, and what HOT Tasking Manager campaigns depend on just as
much as the tracing itself, is (a) splitting an area of interest into a task
grid the way HOT Tasking Manager does, and (b) running the QA/validation
pass every rapid-mapping campaign runs before accepting traced features.
This script does exactly those two things, against **real** OpenStreetMap
data (not synthetic) for a small, extremely densely-mapped area of the
Rohingya camps in Ukhiya, Cox's Bazar -- the product of years of real
Missing Maps/HOT rapid-mapping campaigns since 2017.

Data source: OpenStreetMap via the public Overpass API, (c) OpenStreetMap
contributors, ODbL. Fetched once and cached at
rapid_mapping/cache/osm_raw_response.json -- rerunning this script does not
hit Overpass again.

Run: python3 scripts/rapid_mapping_qa.py
Outputs (all under rapid_mapping/):
  buildings.geojson, roads.geojson   -- parsed from the cached OSM extract
  task_grid.geojson                  -- HOT-Tasking-Manager-style task squares
  qa_flags.csv                       -- every flagged feature + reason
  qa_report.md                       -- summary counts
  before_after.png                   -- task grid only vs. mapped + QA-flagged
"""

import json
import math

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import LineString, Polygon, box

CACHE_PATH = "rapid_mapping/cache/osm_raw_response.json"
AOI = (21.199, 92.149, 21.202, 92.152)  # south, west, north, east
GRID_N = 3  # 3x3 task grid, HOT-Tasking-Manager style

# Flags below are candidates for manual review, not confirmed defects --
# in a densely built camp context, real shelter footprints can legitimately
# be this small, so a human validator (per HOT Tasking Manager's mapped ->
# validated workflow) makes the final call, this script only surfaces them.
MIN_BUILDING_AREA_M2 = 4.0
MIN_ROAD_LENGTH_M = 3.0

OUT_DIR = "rapid_mapping"


def meters_per_degree(lat: float) -> tuple[float, float]:
    lat_m = 111_320.0
    lon_m = 111_320.0 * math.cos(math.radians(lat))
    return lat_m, lon_m


def load_osm_elements() -> list[dict]:
    with open(CACHE_PATH) as f:
        return json.load(f)["elements"]


def elements_to_gdf(elements: list[dict], tag_key: str, geom_type: str) -> gpd.GeoDataFrame:
    rows = []
    for el in elements:
        tags = el.get("tags", {})
        if tag_key not in tags:
            continue
        coords = [(pt["lon"], pt["lat"]) for pt in el.get("geometry", []) if pt]
        if len(coords) < 2:
            continue
        if geom_type == "polygon":
            if coords[0] != coords[-1]:
                coords = coords + [coords[0]]
            try:
                geom = Polygon(coords)
            except Exception:
                continue
        else:
            geom = LineString(coords)
        rows.append({"osm_id": el["id"], "tag_value": tags[tag_key], "geometry": geom})
    return gpd.GeoDataFrame(rows, crs="EPSG:4326")


def build_task_grid(aoi, n) -> gpd.GeoDataFrame:
    south, west, north, east = aoi
    dlat = (north - south) / n
    dlon = (east - west) / n
    cells = []
    task_id = 1
    for row in range(n):
        for col in range(n):
            cell = box(west + col * dlon, south + row * dlat, west + (col + 1) * dlon, south + (row + 1) * dlat)
            cells.append({"task_id": task_id, "status": "MAPPED", "geometry": cell})
            task_id += 1
    return gpd.GeoDataFrame(cells, crs="EPSG:4326")


def qa_buildings(buildings: gpd.GeoDataFrame, lat_m, lon_m) -> pd.DataFrame:
    flags = []
    seen_wkt = {}
    for _, row in buildings.iterrows():
        geom = row.geometry
        reasons = []
        if not geom.is_valid:
            reasons.append(("self_intersecting_or_invalid_polygon", "self-intersecting or invalid polygon"))
        area_m2 = geom.area * lat_m * lon_m
        if area_m2 < MIN_BUILDING_AREA_M2:
            reasons.append(("area_too_small", f"{area_m2:.1f} m^2, below {MIN_BUILDING_AREA_M2} m^2 review threshold"))
        wkt = geom.wkb
        if wkt in seen_wkt:
            reasons.append(("duplicate_geometry", f"duplicate of osm_id {seen_wkt[wkt]}"))
        else:
            seen_wkt[wkt] = row["osm_id"]
        for category, detail in reasons:
            flags.append({"osm_id": row["osm_id"], "feature_type": "building", "reason_category": category, "reason_detail": detail})
    return pd.DataFrame(flags)


def qa_roads(roads: gpd.GeoDataFrame, lat_m, lon_m) -> pd.DataFrame:
    flags = []
    seen_wkt = {}
    for _, row in roads.iterrows():
        geom = row.geometry
        reasons = []
        # rough conversion using local scale factors; adequate at this AOI's scale
        length_m = geom.length * ((lat_m + lon_m) / 2)
        if length_m < MIN_ROAD_LENGTH_M:
            reasons.append(("segment_too_short", f"{length_m:.1f} m, below {MIN_ROAD_LENGTH_M} m review threshold"))
        wkt = geom.wkb
        if wkt in seen_wkt:
            reasons.append(("duplicate_geometry", f"duplicate of osm_id {seen_wkt[wkt]}"))
        else:
            seen_wkt[wkt] = row["osm_id"]
        for category, detail in reasons:
            flags.append({"osm_id": row["osm_id"], "feature_type": "road", "reason_category": category, "reason_detail": detail})
    return pd.DataFrame(flags)


def main():
    elements = load_osm_elements()
    buildings = elements_to_gdf(elements, "building", "polygon")
    roads = elements_to_gdf(elements, "highway", "line")
    buildings.to_file(f"{OUT_DIR}/buildings.geojson", driver="GeoJSON")
    roads.to_file(f"{OUT_DIR}/roads.geojson", driver="GeoJSON")

    grid = build_task_grid(AOI, GRID_N)
    grid.to_file(f"{OUT_DIR}/task_grid.geojson", driver="GeoJSON")

    center_lat = (AOI[0] + AOI[2]) / 2
    lat_m, lon_m = meters_per_degree(center_lat)

    b_flags = qa_buildings(buildings, lat_m, lon_m)
    r_flags = qa_roads(roads, lat_m, lon_m)
    all_flags = pd.concat([b_flags, r_flags], ignore_index=True)
    all_flags.to_csv(f"{OUT_DIR}/qa_flags.csv", index=False)

    flagged_building_ids = set(b_flags["osm_id"]) if not b_flags.empty else set()
    flagged_road_ids = set(r_flags["osm_id"]) if not r_flags.empty else set()

    reason_counts = all_flags["reason_category"].value_counts().to_string() if not all_flags.empty else "None"

    report = f"""# Rapid mapping QA report

Area of interest: {AOI} (south, west, north, east) -- Ukhiya, Cox's Bazar.
Data: real OpenStreetMap extract via Overpass API, (c) OpenStreetMap
contributors, ODbL. Task grid: {GRID_N}x{GRID_N} = {GRID_N * GRID_N} tasks,
HOT-Tasking-Manager-style.

**Flags are candidates for manual review, not confirmed defects** --
per HOT's mapped -> validated workflow, a human validator makes the final
call. In a densely built camp context, a real shelter footprint can
legitimately be a few square metres, so `area_too_small` in particular is a
review queue, not an error list.

| Feature type | Total | Flagged | Flag rate |
|---|---|---|---|
| Buildings | {len(buildings)} | {len(flagged_building_ids)} | {len(flagged_building_ids) / max(len(buildings), 1):.1%} |
| Roads | {len(roads)} | {len(flagged_road_ids)} | {len(flagged_road_ids) / max(len(roads), 1):.1%} |

## Flags by category

{reason_counts}

Full detail (including the specific measurement behind each flag) in `qa_flags.csv`.
"""
    with open(f"{OUT_DIR}/qa_report.md", "w") as f:
        f.write(report)
    print(report)

    fig, axes = plt.subplots(1, 2, figsize=(13, 7))
    grid.boundary.plot(ax=axes[0], color="black", linewidth=1.2)
    for _, row in grid.iterrows():
        c = row.geometry.centroid
        axes[0].annotate(f"TASK {row['task_id']}", (c.x, c.y), ha="center", fontsize=8)
    axes[0].set_title(f"Before: {GRID_N}x{GRID_N} task grid assigned\n(HOT Tasking Manager style)")
    axes[0].set_axis_off()

    grid.boundary.plot(ax=axes[1], color="black", linewidth=1.0)
    buildings.plot(ax=axes[1], color="#4a90d9", edgecolor="none", alpha=0.7)
    if flagged_building_ids:
        buildings[buildings["osm_id"].isin(flagged_building_ids)].plot(ax=axes[1], color="red", edgecolor="none")
    roads.plot(ax=axes[1], color="#333333", linewidth=0.8)
    axes[1].set_title(
        f"After: real OSM buildings ({len(buildings)}) + roads ({len(roads)})\n"
        f"red = QA-flagged ({len(flagged_building_ids)} buildings)"
    )
    axes[1].set_axis_off()

    fig.suptitle("Rapid mapping: task grid + QA pass over a real OSM extract (Ukhiya, Cox's Bazar)", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(f"{OUT_DIR}/before_after.png", dpi=150)
    print(f"wrote {OUT_DIR}/before_after.png")


if __name__ == "__main__":
    main()
