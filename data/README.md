# Data

## `synthetic_site_assessments.csv`
Entirely fabricated (fixed random seed, see `scripts/generate_synthetic_data.py`).
Does not describe any real site, event, or population.

## `cod/bgd_admin3_coxsbazar_subset.geojson`
**Real, public data** — a 6-feature subset of HDX's
[Bangladesh - Subnational Administrative Boundaries](https://data.humdata.org/dataset/cod-ab-bgd)
(COD-AB), source: Bangladesh Bureau of Statistics (BBS) via ITOS, distributed
through UNOCHA ROAP. Filtered from the full 507-upazila `adm3` layer down to
the 6 upazilas the synthetic site data covers (Ukhia, Teknaf, Coxs Bazar
Sadar, Ramu, Chakaria, Naikkhongchhari). Only the boundary polygons are real;
nothing about the synthetic sites placed within them is.

## `upazila_pcode_crosswalk.csv`
Maps this repo's synthetic upazila slugs to the official `adm3_pcode` used by
the boundary file above. Two real name mismatches are documented here on
purpose (e.g. synthetic `ukhiya` vs. official `Ukhia`; `naikhongchhari` vs.
`Naikkhongchhari`) — the join in `scripts/join_needs_choropleth.py` always
goes through this crosswalk's P-codes, never through name matching, which is
exactly what P-codes are for in humanitarian GIS.

## `needs_choropleth_coxsbazar.geojson` / `.png` / `needs_choropleth.qml`
Output of `scripts/join_needs_choropleth.py` — the synthetic site data
aggregated to a composite needs-severity score per upazila, joined onto the
real boundary polygons by P-code, rendered as a static PNG, and shipped with
a QGIS graduated-symbology style (`.qml`) for opening the GeoJSON directly in
QGIS with the same color ramp.

## Regenerating
```
pip install -r requirements.txt geopandas matplotlib
python3 scripts/join_needs_choropleth.py
```
