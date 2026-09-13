# Rapid mapping: task grid + QA validation

## Scope — read this first

Manual imagery tracing in JOSM or the iD editor is a hands-on GUI skill.
Like KoboToolbox and ArcGIS Online in earlier phases, that stays with
whoever actually does it — a script can't honestly perform or claim it.

What *is* scriptable, and what a real HOT Tasking Manager campaign depends
on just as much as the tracing itself, is:

1. **Splitting an area of interest into a task grid** — how HOT Tasking
   Manager organizes rapid-mapping campaigns into assignable squares.
2. **The QA/validation pass** every campaign runs before accepting traced
   features, following HOT's mapped → validated workflow.

This phase builds both, and runs them against **real** OpenStreetMap data
(not synthetic) — a small area in Ukhiya, Cox's Bazar, one of the most
densely mapped places on Earth thanks to years of real Missing Maps/HOT
rapid-mapping campaigns following the 2017 Rohingya refugee influx.

## What's here

- `cache/osm_raw_response.json` — the raw Overpass API response, fetched
  once and cached (rerunning `scripts/rapid_mapping_qa.py` does not hit
  Overpass again — public infrastructure, fetched courteously)
- `buildings.geojson`, `roads.geojson` — parsed from the cache: **693 real
  building footprints, 71 real road segments**, all already mapped by real
  volunteers, not fabricated by this repo
- `task_grid.geojson` — a 3×3 HOT-Tasking-Manager-style task grid over the
  same area
- `qa_flags.csv` / `qa_report.md` — every flagged feature, with the specific
  measurement behind the flag (self-intersecting polygons, duplicate
  geometries, footprints/segments below a size threshold)
- `before_after.png` — left: the task grid as assigned; right: the same
  grid with the real mapped buildings/roads overlaid, QA-flagged buildings
  in red

## On the QA flags

38 of 693 buildings (5.5%) are flagged, all for being smaller than a 4 m²
review threshold — **candidates for manual review, not confirmed errors**.
In a densely built camp context a real shelter footprint can legitimately
be a few square metres, so a human validator makes the final call, exactly
as HOT's own mapped → validated workflow works. This script surfaces the
review queue; it doesn't adjudicate it.

## Data source and license

OpenStreetMap data via the public Overpass API. © OpenStreetMap
contributors, available under the [Open Database License
(ODbL)](https://www.openstreetmap.org/copyright).

## Regenerating

```
python3 scripts/rapid_mapping_qa.py
```
