# Kobo/ODK vs. Survey123: what changed and why

Two XLSForms in this repo implement the same instrument:

- `rapid_assessment_form.xlsx` — standard ODK XLSForm, deployed on
  KoboToolbox
- `rapid_assessment_form_survey123.xlsx` — the Survey123 dialect,
  imported via Survey123 Connect into ArcGIS Online

Same questions, same skip logic, same choice lists. The differences below
are the real, documented constraints of the Esri stack, verified against
Esri's own XLSForm documentation — not stylistic choices.

## 1. One geometry field per record

An ArcGIS feature layer has exactly one `SHAPE` column, so a Survey123 form
may use only **one** geo question (`geopoint`/`geotrace`/`geoshape`) as the
record's actual geometry. This form has two geo questions — the required
`gps_point` and the optional `site_boundary` — so `site_boundary` gets
`bind::esri:fieldType` set to the literal value `null`. That tells Survey123
Connect to keep it as a normal attribute rather than a second geometry,
which is Esri's documented workaround for forms with multiple map
questions. `gps_point` is left with the field type blank, so Survey123
Connect auto-maps it to the layer's point geometry.

## 2. Esri custom columns for explicit field typing

Kobo/ODK infers a reasonable SQLite/CSV export type from the question type
alone. Survey123 lets you be explicit with `bind::esri:fieldType` and
`bind::esri:fieldLength`, controlling exactly what field type/length gets
created in the ArcGIS feature layer (e.g. `site_id` → `esriFieldTypeString`,
length 20; `hh_estimate` → `esriFieldTypeInteger`). Left blank everywhere
else, Survey123 Connect infers the same reasonable defaults Kobo does.

## 3. No hints on `begin group`

Kobo/ODK renders a hint attached to a `begin group` row above that group's
questions. Survey123 does not render group-level hints at all. The
protection module's guidance ("aggregate, site-level indicators only — no
individually identifying information") was carried by both the group hint
*and* a separate `note` question in the Kobo version; the Survey123 version
drops the now-redundant group hint and keeps the `note` question, so nothing
is lost.

## 4. Validation coverage is asymmetric — and that's expected

`rapid_assessment_form.xlsx` is validated end-to-end with `xls2xform`
(open-source, part of the standard ODK/Kobo toolchain) — it produces a real,
loadable XForm.

`rapid_assessment_form_survey123.xlsx` cannot be validated the same way:
`xls2xform` doesn't recognize the `esri:` XML namespace Survey123 Connect
injects for its custom columns, and fails with `the prefix "esri" ... is not
bound`. This isn't a bug in the form — it's the actual dividing line between
the two ecosystems: **compiling** a Survey123-dialect XLSForm requires
Survey123 Connect itself (proprietary, ArcGIS-account-gated), and there's no
open equivalent. What this repo does instead: strip the two `bind::esri:*`
columns and re-validate with `xls2xform` to confirm the underlying question
set, skip logic, and choice lists are still valid XLSForm (they are — see
`scripts/build_xlsform_survey123.py`'s test in CI/local runs); the
Esri-specific columns are checked by hand against Esri's documented column
names and accepted values rather than by an automated tool.

## Everything else is identical

`text`, `integer`, `decimal`, `date`, `select_one`, `select_multiple`,
`geopoint`, `geoshape`, `note`, `begin group`/`end group`, `relevant`,
`constraint`, `choice_filter` — all supported the same way in both dialects.
The question set, the Bangla/English labels, and the skip logic did not
change between the two forms.
