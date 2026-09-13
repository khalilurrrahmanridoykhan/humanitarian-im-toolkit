# Results

One row per phase, real numbers only — updated as each phase actually ran,
not projected in advance. Same discipline as this account's other repos.

| Phase | What was proven | Real numbers |
| :--- | :--- | :--- |
| R1 | Multi-sector rapid assessment XLSForm compiles end-to-end via `xls2xform` (the actual ODK/Kobo toolchain, not just a spreadsheet that looks right) | 9 modules, skip logic on 2 conditional branches, Bangla+English labels on every question, 18-site synthetic dataset generated deterministically |
| R2 | Survey123 dialect adaptation, including the real one-geometry-per-feature-layer constraint | `bind::esri:fieldType=null` workaround verified against Esri's own docs; confirmed (not assumed) that `xls2xform` cannot parse the `esri:` namespace by stripping those 2 columns and re-validating the rest cleanly |
| R3 | Join to real Bangladesh administrative boundaries on official P-code, not name | 6/6 upazilas matched via HDX COD-AB (BBS/ITOS); 2 of those 6 had a real slug/official-name mismatch (`ukhiya`/`Ukhia`, `naikhongchhari`/`Naikkhongchhari`) that a name-based join would have hit |
| R4 | Rapid-mapping task grid + QA validation against a **real** OSM extract (not synthetic) | 693 real buildings + 71 real roads (Ukhiya, Cox's Bazar), fetched once via Overpass and cached; 38 buildings (5.5%) flagged for manual review, framed as a review queue not an error list |
| R5 | 4W dashboard actually launched and driven with a headless browser, not just trusted to compile | Caught and fixed a real bug: `px.scatter_map` rendered blank in this Plotly/Streamlit combination; switched to `px.scatter_mapbox`, re-verified with screenshots in both default and filtered states |
| R6 | Documented, file-based join to `geohealth-risk-mapping`'s hazard layer | Checked that project's real state directly: its risk-score phase (H10) doesn't exist yet and its one real zonal-stats file keys by name, not P-code — documented the contract and recommendation, demonstrated the join mechanism against a clearly-labeled placeholder |

## Notes

- Every phase used **synthetic or clearly-labeled placeholder data** except
  R3's administrative boundaries and R4's OSM extract, which are real public
  data — see each phase's own README for the exact provenance.
- No live account (KoboToolbox, ArcGIS Online, OSM) was created or used by
  either the user or this toolkit at any phase — see `docs/ROADMAP.md`'s
  scope note.
