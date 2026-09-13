# 4W dashboard

`app.py` is a Streamlit dashboard following the standard cluster-coordination
4W/5W template structure: Who (partner organization), What (sector/activity),
Where (site/upazila), When (status/start date).

Built entirely from this repo's own synthetic/fictional data:
- Sites and their sectors of need: Phase R1's `data/synthetic_site_assessments.csv`
- Activities: `data/fictional_4w_activities.csv` (`scripts/generate_4w_data.py`)
  — a fabricated partner/activity list. **The partner organization names are
  invented for this demonstration and do not refer to any real organization.**

No real organization, site, or population data anywhere in this dashboard.

## Running it

```
pip install -r requirements.txt
streamlit run dashboard/app.py
```

Like the earlier phases, going live on a public URL (e.g. Streamlit
Community Cloud) needs an account and isn't done here — see
`screenshots/` for a verified local run instead: filter sidebar (sector,
upazila, partner, status), summary KPI row, a site map sized/colored by
activity count, sector/status charts, and the filtered activity table, all
confirmed to update together when a filter is applied.

## Regenerating the underlying data

```
python3 scripts/generate_4w_data.py
```
