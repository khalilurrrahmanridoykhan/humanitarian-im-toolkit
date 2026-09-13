# Humanitarian IM & Rapid Mapping Portfolio — Plan

Build a **project-based portfolio** proving the Kobo/ODK + Field Maps + rapid-mapping
skill set for **humanitarian & disaster response** roles — IOM NPM (Needs & Population
Monitoring), UNHCR, REACH, BRAC HCMP (Cox's Bazar), DDM, CARE. This is not learning from
zero: it packages and extends the field-data/GIS experience already proven in
production at GMGI and MORU/BRAC (see §0), closes the specific tool gaps those
employers screen for, and produces public evidence a recruiter can click through —
same as every other repo in this portfolio.

Same working discipline as the Prohori/Geospatial-AI plans: **one branch → one PR
(`Phase Rx — <name>`) → merge → tag `phase-rx`**, granular commits, every phase ends
with a **"Done when"** gate, one public note/screenshot per phase.

**Repo (to create):** `github.com/khalilurrrahmanridoykhan/humanitarian-im-toolkit`
**Related:** `Geospatial AI for Public Health — Plan.md` (Bangladesh disaster-risk
layer this can feed into), [[project_geohealth_ai]], [[project_ph_repo_auditor]]
(same "verify against a real instance" discipline).

---

## 0. Baseline — what's already proven (don't relearn this)

From `RidoyCV_MasterData.json`:

- **ODK + KoBoToolbox** deployed for field programs, production (GMGI, 2025–present).
- **QGIS** spatial support for field data (GMGI).
- **BRAC Microstratification System** — production village-level malaria reporting,
  **11,448 GPS-referenced villages**, 5 districts, full geographic hierarchy
  (Division → District → Upazila → Union → Ward → Village), Bangla/English village
  names, role-based data-quality workflow. This is a real, live, large-scale field
  data + geospatial system — the strongest single evidence point for an NPM/IM role.
- **NMEP/NMCP data collection + mapping portals** — field-to-dashboard pipelines,
  government production.
- SPSS / Stata / R / SurveyCTO alongside Kobo/ODK.
- `geohealth-risk-mapping` — Sentinel-2 satellite risk mapping for Bangladesh (H0–H1
  done), i.e. already building the disaster-risk half of this picture.

**What this plan actually needs to add**, based on what IOM/UNHCR/REACH/DDM job specs
ask for that isn't in the CV yet:

| Gap | Why it matters | Closed in |
|---|---|---|
| Esri ArcGIS Online / Field Maps / Survey123 | Most UN/INGO IM units standardize on Esri, not just QGIS | Phase R2 |
| Common Operational Datasets (COD-AB) / P-codes | The humanitarian GIS lingua franca (HDX, OCHA) — admin joins must use P-codes | Phase R3 |
| Rapid mapping (HOT Tasking Manager, JOSM/iD) | "Rapid mapping" as a named skill = OSM building/road tracing from imagery for disaster response | Phase R4 |
| 4W/5W IM products | Standard cluster-coordination deliverable ("Who's doing What, Where, When [for Whom]") | Phase R5 |
| DTM / MSNA-style multi-sector assessment form design | IOM DTM and REACH MSNA are the reference instruments this sector uses | Phase R1 |

---

## 1. Rules

- One branch → one PR (`Phase Rx — <name>`) → merge → tag `phase-rx`. `main` always
  demoable.
- **Synthetic / public data only.** Never use real Rohingya, camp-resident, or any
  other real beneficiary/household-level data — same ethics line as the BRAC and
  geohealth work. Simulate a Cox's Bazar-style camp (fake camp/block IDs, fake names)
  or use genuinely public datasets (HDX CODs, OSM).
- Every phase: a short README/note explicitly mapping what it demonstrates to the
  vocabulary in real job ads (pull 2–3 live IOM/UNHCR/REACH postings from the existing
  ReliefWeb digest pipeline and quote the exact line each phase answers).
- Free tiers only: KoboToolbox free account, ArcGIS Online free/trial tier, OSM/JOSM
  (free), HDX (free), Streamlit Community Cloud.

---

## 2. Phases

### Phase R0 — Gap audit against real job ads
Pull 5–10 real IOM NPM / UNHCR IM / REACH Assessment Officer / DDM postings (the
digest already tracked at `RIDOY/JOB/OnlineJobs/` is a source). Extract the recurring
required-skill phrases verbatim. Build a one-page matrix: skill phrase → existing
evidence (BRAC system, NMEP, etc.) or → which phase in this plan will produce it.
- **Done when:** the matrix exists and every phase below is traceable to at least one
  real job-ad line.

### Phase R1 — Multi-sector rapid assessment form (Kobo/ODK)
Design an XLSForm mirroring IOM DTM Site Assessment / REACH MSNA structure: shelter,
WASH, health, protection modules, skip logic, GPS point + geoshape (camp/site boundary)
capture, Bangla/English labels. Deploy on KoboToolbox. Collect synthetic responses for
a fictional Cox's Bazar-style camp (10–20 fake sites).
- **Done when:** live Kobo form + exported dataset + a README explaining the DTM/MSNA
  design choices.

### Phase R2 — Esri parity build (ArcGIS Field Maps / Survey123)
Rebuild the same instrument in Survey123, publish to ArcGIS Online, collect the same
synthetic data via Field Maps (mobile, offline-capable). Document side-by-side with
Phase R1 so the portfolio explicitly shows fluency in **both** stacks — Kobo/ODK (most
common at BRAC/national NGOs) and Esri (most common inside UN agencies).
- **Done when:** public/shareable ArcGIS Online map + a Kobo-vs-Field-Maps comparison
  note.

### Phase R3 — CODs / P-codes join + needs choropleth
Pull Bangladesh COD-AB boundaries and P-codes from HDX. Join the Phase R1/R2 synthetic
site data at Upazila/Union level (reusing the geographic-hierarchy pattern already
proven in the BRAC system). Produce a needs/severity choropleth in QGIS.
- **Done when:** a QGIS project + exported map that joins cleanly on official P-codes,
  no manual name-matching.

### Phase R4 — Rapid mapping (HOT-style)
Trace buildings and roads from satellite imagery in JOSM or the iD editor for a
disaster-affected AOI — either a real open HOT Tasking Manager project (contribute for
real, if one is active and appropriate) or a documented synthetic exercise if not.
Record the workflow: task selection, validation rules, QA.
- **Done when:** a documented, reproducible rapid-mapping session with before/after
  imagery and a feature count, and (if real) a HOT contribution link.

### Phase R5 — 4W/5W IM dashboard
Build a "Who's doing What, Where, When" operational dashboard from the synthetic
assessment data + a fictional partner/activity list — same dashboard muscle as the
DHIS2/malaria dashboards already shipped, restyled to match real OCHA/UNHCR 4W/5W
templates (site, sector, partner, status columns; map + table views).
- **Done when:** public Streamlit (or similar) dashboard matching a real 4W/5W template
  structure, with the source template linked in the README.

### Phase R6 — Integration + portfolio packaging
Link this toolkit to `geohealth-risk-mapping` as an optional "population/needs overlay"
on the disaster-risk layers (no code coupling required — a documented join path is
enough). Publish the repo, write a README that opens with the job-ad mapping from
Phase R0. Add a `humanitarian_im_field_data` project entry to
`RidoyCV_MasterData.json` and generate a tailored CV/cover-letter variant for
NPM/IM/Assessment Officer roles (reuse the CV-generation scripts pattern in
`RIDOY/CV/`).
- **Done when:** public repo live, CV master data updated, one tailored CV variant
  generated.

---

## 3. Suggested schedule

Each phase is scoped to be a weekend-to-one-week effort given the existing baseline —
this is packaging + targeted gap-filling, not learning field data collection from
scratch. R0 first (cheap, de-risks the rest by anchoring every later phase to real job
language); R1–R2 can run close together since they're the same instrument twice; R3–R5
can reorder based on which upcoming job ad matters most.
