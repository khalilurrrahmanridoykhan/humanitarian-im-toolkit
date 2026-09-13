# Multi-sector rapid site assessment form

`rapid_assessment_form.xlsx` is an XLSForm (built by `scripts/build_xlsform.py`,
validated with `xls2xform`) for a multi-sector rapid site assessment, in the
style of a IOM DTM site assessment or a REACH MSNA-type instrument: one
enumerator visit produces one **site-level** record, not individual
household or person data.

## Structure

- **Metadata** — enumerator, date, site ID/name
- **Location** — cascading division → district → upazila selects, a
  required `geopoint` for the site's location, and an optional `geoshape`
  for the site boundary
- **Site profile** — type, status, household/population estimates
- **Shelter** — majority shelter type; damage-percentage questions only
  trigger (`relevant`) when the site reports a recent disaster
- **WASH** — water source, functionality, latrine ratio
- **Health** — on-site facility check with a conditional distance question
- **Protection** — **site-level aggregate indicators only**; the group
  opens with an explicit note that no individually identifying information
  is collected
- **Priority needs** — top-3 sector ranking with a `constraint` preventing
  duplicate picks
- **Closing** — free-text remarks, optional photo

Every question has both `label::English (en)` and `label::Bangla (bn)`.
Skip logic uses `relevant`; range/order checks use `constraint`.

## Data protection

This form only ever produces aggregate, site-level records — no names, no
individual ages, no household-identifying detail beyond the site itself.
`data/synthetic_site_assessments.csv` is entirely fabricated (fixed random
seed) and does not describe any real location, event, or population.

## Regenerating

```
pip install pyxform openpyxl
python3 scripts/build_xlsform.py
xls2xform forms/rapid_assessment_form.xlsx forms/rapid_assessment_form.xml
python3 scripts/generate_synthetic_data.py
```

## Deploying

Upload `rapid_assessment_form.xlsx` directly in KoboToolbox
(`kf.kobotoolbox.org` → New → Upload an XLSForm), or via the Kobo API with a
personal access token. Deployment isn't automated here since it requires a
Kobo account.

## Esri Survey123 version

`rapid_assessment_form_survey123.xlsx` is the same instrument adapted to the
Survey123 XLSForm dialect (built by
`scripts/build_xlsform_survey123.py`). See `kobo-vs-survey123.md` for the
concrete, documented differences between the two dialects and why each one
exists. Like the Kobo form, deployment (importing into Survey123 Connect,
publishing to ArcGIS Online) isn't automated here since it requires an
ArcGIS account.
