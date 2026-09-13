# Roadmap

Same working discipline as this account's other projects: one branch → one PR
(`Phase Rx — <name>`) → merge → tag `phase-rx`, granular commits, `main`
always demoable. **Synthetic / public data only** at every phase — no real
Rohingya, camp-resident, or other real beneficiary/household-level data.

## Phase R1 — Multi-sector rapid assessment form (Kobo/ODK)
Multi-module XLSForm (shelter, WASH, health, protection) with skip logic,
GPS point + geoshape (site/camp boundary) capture, Bangla/English labels.
Deployed on KoboToolbox against a synthetic site dataset.
- **Done when:** live Kobo form + exported dataset + a README documenting
  the instrument design.

## Phase R2 — Esri ArcGIS Field Maps / Survey123 parity
The same instrument rebuilt in Survey123, published to ArcGIS Online, with
data collected via Field Maps (mobile, offline-capable) — demonstrating both
the Kobo/ODK and Esri stacks side by side.
- **Done when:** shareable ArcGIS Online map + a Kobo-vs-Field-Maps
  comparison note.

## Phase R3 — Administrative-boundary (COD/P-code) integration
Bangladesh Common Operational Dataset boundaries and P-codes (from HDX)
joined to the Phase R1/R2 data at Upazila/Union level, producing a
needs/severity choropleth in QGIS.
- **Done when:** a QGIS project that joins cleanly on official P-codes, no
  manual name-matching.

## Phase R4 — Rapid mapping
Building and road tracing from satellite imagery (JOSM or the iD editor) for
a disaster-affected area of interest, following HOT Tasking Manager
conventions (task selection, validation rules, QA).
- **Done when:** a documented, reproducible mapping session with
  before/after imagery and a feature count.

## Phase R5 — Operational dashboard (4W/5W)
A "Who's doing What, Where, When" dashboard built from the synthetic
assessment data and a fictional partner/activity list, following standard
cluster-coordination dashboard conventions (site, sector, partner, status;
map + table views).
- **Done when:** a public dashboard matching a real 4W/5W template structure.

## Phase R6 — Integration & documentation
Connect this toolkit to `geohealth-risk-mapping` as an optional
population/needs overlay on the hazard layers (a documented join path, no
code coupling required), and finish end-to-end documentation for the repo.
- **Done when:** the join path is documented and demoable end-to-end.
