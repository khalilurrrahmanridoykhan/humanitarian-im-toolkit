# Integration with geohealth-risk-mapping

A documented, file-based join path between this toolkit's population/needs
data and the hazard-risk layers from
[`geohealth-risk-mapping`](https://github.com/khalilurrrahmanridoykhan/geohealth-risk-mapping)
(Sentinel-1/2 + Google Earth Engine dengue/flood risk mapping for
Bangladesh). **No code coupling** — neither repo imports the other; the
contract is a shared P-code join key on a plain CSV/GeoJSON file.

## Current state (checked directly, not assumed)

Before writing this, the actual state of both repos was checked rather than
assumed:

- `geohealth-risk-mapping`'s own `PLAN.md` places its ward-level **risk
  score** — the thing this integration ultimately wants — at **Phase H10**
  ("combine GLM/INLA and an XGBoost + SHAP model; produce a normalized
  ward-level risk score"). As of this writing that project has completed
  through **H7**; H10 doesn't exist yet.
- Its one real zonal-stats output so far,
  `data/processed/dhaka_smoke_tile_zonal_stats.csv`, keys admin units by
  plain district **name** (`Dhaka`, `Gazipur`, `Narayanganj`) — not a
  P-code.
- Its area of interest so far (Dhaka/Gazipur/Narayanganj for zonal stats,
  Sunamganj for the real SAR flood mapping in H5) doesn't overlap this
  toolkit's Cox's Bazar-area synthetic data either.

So there is no real file to join to today. What follows is the contract for
when there is, demonstrated now against a placeholder.

## The join contract

| | This toolkit (`humanitarian-im-toolkit`) | `geohealth-risk-mapping` (once it reaches H10) |
|---|---|---|
| Output | `data/needs_choropleth_coxsbazar.geojson` (Phase R3) | a ward/upazila-level risk-score table |
| Join key | `adm3_pcode` (official HDX COD-AB P-code) | **recommended: also `adm3_pcode`** |
| Score column | `needs_score` (0-100) | `hazard_score` / `risk_score` (whatever scale H10 lands on) |

**Recommendation for `geohealth-risk-mapping`'s H10 (documentation only —
this repo doesn't modify that one):** join its ward-level output to HDX
COD-AB **P-codes**, not admin names, before combining it with anything
else. This isn't a hypothetical concern — Phase R3 of *this* toolkit hit it
directly: the synthetic data's own upazila slugs didn't match the official
COD-AB names (`ukhiya` vs. official `Ukhia`, `naikhongchhari` vs. official
`Naikkhongchhari`). A name-based join silently drops or misjoins rows in
exactly that situation; `geohealth-risk-mapping`'s current zonal-stats
output already keys by plain name, which is the same failure mode waiting
to happen once it needs to join against another P-coded dataset (health
facility data, population data, or this toolkit's needs data).

## Demonstrating the join today

`scripts/join_hazard_needs_overlay.py` implements the join against this
toolkit's real Phase R3 output and a clearly-labeled placeholder hazard
table (`data/geohealth_integration/mock_hazard_placeholder.csv`, values
fabricated, explicitly marked `SYNTHETIC_PLACEHOLDER`) built to the schema
above. Run:

```
python3 scripts/join_hazard_needs_overlay.py
```

Outputs `data/geohealth_integration/combined_priority_coxsbazar.geojson`
and a three-panel render (needs score / placeholder hazard score / combined
priority score) — proving the join mechanism end-to-end. **The moment
`geohealth-risk-mapping` produces a real P-coded ward/upazila risk table for
an overlapping area, that file replaces
`mock_hazard_placeholder.csv` and this script's output stops being a
demonstration.**
