# Humanitarian IM & Rapid Mapping Toolkit

A field-data and mapping toolkit for humanitarian and disaster-response
information management — multi-sector rapid assessment (Kobo/ODK), Esri
ArcGIS Field Maps/Survey123 interoperability, administrative-boundary
(COD/P-code) integration, rapid mapping from satellite imagery, and
operational 4W/5W dashboards.

Builds on the geospatial and field-data-systems work in
[`geohealth-risk-mapping`](https://github.com/khalilurrrahmanridoykhan/geohealth-risk-mapping)
(Sentinel-1/2, Google Earth Engine, hazard mapping) and applies the same
disciplined, verify-against-a-real-source approach used throughout this
account's other repos.

**Synthetic / public data only** — no real beneficiary, camp-resident, or
displaced-population data is used anywhere in this repo.

## Contents

- `forms/` — the multi-sector rapid site assessment XLSForm (Kobo/ODK + Survey123) — see `forms/README.md`
- `data/` — synthetic site-assessment dataset, real HDX administrative boundaries, and the P-code join/choropleth — see `data/README.md`
- `rapid_mapping/` — task grid + QA validation over a real OpenStreetMap extract — see `rapid_mapping/README.md`
- `dashboard/` — a 4W/5W Streamlit dashboard over the synthetic data — see `dashboard/README.md`
- `scripts/` — all build/join/QA/data-generation scripts, each reproducible from source

## Roadmap and results

`docs/ROADMAP.md` — the phase-by-phase build plan (all 6 phases complete).
`RESULTS.md` — real numbers per phase. `docs/geohealth-integration.md` — the
documented join path to `geohealth-risk-mapping`'s hazard layers.
