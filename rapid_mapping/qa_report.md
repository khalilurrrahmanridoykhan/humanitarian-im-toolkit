# Rapid mapping QA report

Area of interest: (21.199, 92.149, 21.202, 92.152) (south, west, north, east) -- Ukhiya, Cox's Bazar.
Data: real OpenStreetMap extract via Overpass API, (c) OpenStreetMap
contributors, ODbL. Task grid: 3x3 = 9 tasks,
HOT-Tasking-Manager-style.

**Flags are candidates for manual review, not confirmed defects** --
per HOT's mapped -> validated workflow, a human validator makes the final
call. In a densely built camp context, a real shelter footprint can
legitimately be a few square metres, so `area_too_small` in particular is a
review queue, not an error list.

| Feature type | Total | Flagged | Flag rate |
|---|---|---|---|
| Buildings | 693 | 38 | 5.5% |
| Roads | 71 | 0 | 0.0% |

## Flags by category

reason_category
area_too_small    38

Full detail (including the specific measurement behind each flag) in `qa_flags.csv`.
