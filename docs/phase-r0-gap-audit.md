# Phase R0 — Gap audit against real job ads

**Method:** pulled current/recent job descriptions for the four target org types
(IOM, UNHCR, REACH, CARE-adjacent MEAL) via public search, quoted their exact
technical-requirement language, and matched each phrase against either (a)
existing evidence already in `RidoyCV_MasterData.json` / this portfolio, or (b)
the plan phase that will produce it. Every phase in `docs/PLAN.md` traces to at
least one row below.

## Source job ads

- REACH GIS Officer (Nairobi/Horn of Africa) — remote sensing + GIS analyst role
- IOM DTM (Displacement Tracking Matrix) Project/Reporting/Information
  Management Officer postings — multiple (impactpool.org, myjobmag.com, dtm.iom.int)
- UNHCR Associate/Assistant Information Management Officer (GIS) — multiple
  postings (impactpool.org, reliefweb.int, ngojobsinafrica.com)
- CARE / MEAL Officer postings (Save the Children, IRC, BRAC as comparators —
  same technical-skill pattern across the sector)

## Gap matrix

| Requirement phrase (quoted from a real ad) | Source | Existing evidence | Plan phase |
|---|---|---|---|
| "expertise in data collection tools such as Kobo and ODK", "proven skills working with mobile data collection software (KoBO, ODK, ONA)", "using XLS forms for ODK and Kobo" | IOM DTM | ✅ Already covered — ODK + KoBoToolbox deployed for field programs at GMGI (production); NMEP data-collection portal | Deepened in **R1** (DTM/MSNA-style multi-sector instrument, XLSForm skip logic) |
| "geo-data collection and field mapping exercises" | UNHCR IM Officer | ✅ Already covered — BRAC Microstratification System, 11,448 GPS-referenced villages, production | Cite directly; no new build needed |
| "advanced knowledge of Google Earth Engine" | REACH GIS Officer | ✅ Already covered — `geohealth-risk-mapping` Phase H1 (GEE + STAC cloud data access) | Cite directly |
| "sound foundational knowledge of remote sensing... spatial/geostatistical analysis... hazard/environmental monitoring (flood, drought, landslide)" | REACH GIS Officer / UNHCR IM Officer | ✅ Already covered — `geohealth-risk-mapping` H0–H6 (Sentinel-2, Sentinel-1 SAR flood mapping, U-Net segmentation, zonal stats, drone YOLO) | Cite directly |
| "demonstrated knowledge of R, STATA, Python" | REACH GIS Officer / IOM DTM | ✅ Already covered — SPSS/Stata/R/Python throughout CV | Cite directly |
| "knowledge of Relational Database Management Systems (RDBMS)" | IOM DTM | ✅ Already covered — MySQL/PostgreSQL/MongoDB, schema design | Cite directly |
| "GIS smartphone applications (**ArcGIS Field Maps, Survey 123**, Qfield, OsmAnd)" | UNHCR IM Officer (GIS) | ❌ Gap — QGIS only, no Esri stack evidence | **R2** — Esri Field Maps/Survey123 parity build |
| "excellent skills and experience in ESRI suite software... ArcPro, ArcMap, ArcGIS Online" | UNHCR IM Officer (GIS) | ❌ Gap | **R2** |
| "experience with open-source solutions (QGIS, **PostGIS**, Geoserver)" | UNHCR IM Officer (GIS) | ⚠️ Partial — QGIS support experience exists, PostGIS installed locally but no shipped project using it yet | **R3** — CODs/P-code join in QGIS+PostGIS |
| "knowledge of commonly used data sources (**HDX, OSM, GeoNames**)" | UNHCR IM Officer (GIS) | ❌ Gap | **R3** (HDX CODs/P-codes) + **R4** (OSM rapid mapping) |
| implicit sector term: rapid mapping / building & road tracing for disaster response (HOT Tasking Manager convention) | Sector-standard, not a single ad quote | ❌ Gap | **R4** |
| "interactive dashboards in MS PowerBI and/or Tableau" | IOM DTM | ⚠️ Partial — Streamlit + R Shiny dashboards shipped (DHIS2 malaria case study, malaria tracker), but no PowerBI/Tableau artifact | **R5** — note tool-transferability explicitly in the dashboard's README rather than rebuilding in a licensed tool |
| "data protection guidelines and principles" for displacement/beneficiary data | IOM DTM | ⚠️ Partial — role-based access + approval workflow shipped in the BRAC system, but not framed around *displacement-specific* data protection (IOM/UNHCR data protection principles) | **R1** — explicit ethics/data-protection section in the assessment-form README |

## Reading this matrix

Nine of thirteen requirement lines are **already backed by shipped, production
work** — this portfolio's job is to make that evidence legible to a
recruiter (cite it in one place, in the sector's own vocabulary), not to build
it from scratch. The four real gaps (Esri stack, HDX/OSM/P-codes, rapid
mapping, and framing existing dashboard work against PowerBI/Tableau
expectations) are exactly what phases R2–R5 close.
