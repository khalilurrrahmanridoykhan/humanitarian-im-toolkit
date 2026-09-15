"""4W/5W operational dashboard -- Who's doing What, Where, When (for Whom).

Follows the standard cluster-coordination 4W/5W template structure: a
partner/sector/site/status activity table, map + table views, and summary
counts. Built entirely from this repo's synthetic/fictional data --
Phase R1's synthetic site assessments and a fictional partner-activity list
(scripts/generate_4w_data.py). No real organization, site, or population
data.

Color system follows the project's dataviz skill: a validated 8-hue
categorical palette (run `node scripts/validate_palette.js` in that skill
to reproduce), a single sequential blue ramp for magnitude (the map), and a
one-hue ordinal ramp for the status donut, since status here is a sequence
(planned -> ongoing -> completed), not an unordered category. The sector
bar chart deliberately uses ONE color for every bar -- the axis labels
already carry sector identity, so coloring each bar differently would just
be spending the identity channel to re-say what the bar's own label shows.

Run: streamlit run dashboard/app.py
"""

import json

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="4W Dashboard -- Rapid Assessment Sites", layout="wide")

SITES_CSV = "data/synthetic_site_assessments.csv"
ACTIVITIES_CSV = "data/fictional_4w_activities.csv"
BOUNDARIES_GEOJSON = "data/cod/bgd_admin3_coxsbazar_subset.geojson"
CROSSWALK_CSV = "data/upazila_pcode_crosswalk.csv"

# --- Palette (dark mode, validated -- see module docstring) -----------------
SURFACE = "#1a1a19"        # chart surface (matches secondaryBackgroundColor)
PAGE = "#0d0d0d"
INK_PRIMARY = "#ffffff"
INK_SECONDARY = "#c3c2b7"
INK_MUTED = "#898781"
GRIDLINE = "#2c2c2a"

CATEGORICAL_1 = "#3987e5"  # slot 1, blue -- single-series bar chart color
CATEGORICAL_2 = "#d95926"  # slot 2, orange -- site markers, contrasts against the blue choropleth fill

# Sequential blue ramp (light -> dark), used for the map's magnitude encoding
SEQUENTIAL_BLUE = [
    [0.0, "#cde2fb"], [0.15, "#9ec5f4"], [0.3, "#6da7ec"],
    [0.45, "#3987e5"], [0.6, "#256abf"], [0.8, "#1c5cab"], [1.0, "#0d366b"],
]

# Ordinal one-hue ramp for workflow status (order carries meaning: planned ->
# ongoing -> completed), lightness increases toward the dark surface so the
# more-advanced state stays more visible, not less.
STATUS_ORDER = ["planned", "ongoing", "completed"]
STATUS_COLORS = {"planned": "#1c5cab", "ongoing": "#3987e5", "completed": "#86b6ef"}

CHART_FONT = dict(family="system-ui, -apple-system, 'Segoe UI', sans-serif", color=INK_SECONDARY)


def style_chart(fig, height, legend=False):
    fig.update_layout(
        height=height,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE,
        font=CHART_FONT,
        showlegend=legend,
        legend=dict(font=dict(color=INK_SECONDARY)) if legend else None,
    )
    fig.update_xaxes(gridcolor=GRIDLINE, linecolor=GRIDLINE, zerolinecolor=GRIDLINE, tickfont=dict(color=INK_MUTED))
    fig.update_yaxes(gridcolor=GRIDLINE, linecolor=GRIDLINE, zerolinecolor=GRIDLINE, tickfont=dict(color=INK_MUTED))
    return fig


@st.cache_data
def load_data():
    sites = pd.read_csv(SITES_CSV)
    activities = pd.read_csv(ACTIVITIES_CSV)
    gps = sites["location/gps_point"].str.split(" ", expand=True)
    sites["lat"] = gps[0].astype(float)
    sites["lon"] = gps[1].astype(float)

    with open(BOUNDARIES_GEOJSON) as f:
        boundaries = json.load(f)
    crosswalk = pd.read_csv(CROSSWALK_CSV)
    # Same P-code join as Phase R3/R6 -- never join upazila boundaries by
    # name, the crosswalk exists specifically because slugs and official
    # COD-AB names don't always match (see data/README.md).
    activities = activities.merge(
        crosswalk[["synthetic_upazila_slug", "official_adm3_pcode"]],
        left_on="upazila", right_on="synthetic_upazila_slug", how="left",
    )
    return sites, activities, boundaries, crosswalk


sites, activities, boundaries_geojson, crosswalk = load_data()

st.markdown(
    """
    <style>
    div[data-testid="stMetric"] {
        background-color: #1a1a19;
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 8px;
        padding: 14px 16px 10px 16px;
    }
    div[data-testid="stMetricLabel"] { color: #c3c2b7; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("4W Dashboard: Who's Doing What, Where, When")
st.caption(
    "Demonstration dashboard built entirely from synthetic/fictional data "
    "(Phase R1 synthetic site assessments + a fabricated partner-activity list). "
    "No real organization, site, or population data."
)

with st.sidebar:
    st.header("Filters")
    sector_opts = sorted(activities["sector"].unique())
    upazila_opts = sorted(activities["upazila"].unique())
    partner_opts = sorted(activities["partner_org"].unique())
    status_opts = [s for s in STATUS_ORDER if s in activities["status"].unique()]

    f_sector = st.multiselect("Sector", sector_opts, default=sector_opts)
    f_upazila = st.multiselect("Upazila", upazila_opts, default=upazila_opts)
    f_partner = st.multiselect("Partner organization", partner_opts, default=partner_opts)
    f_status = st.multiselect("Status", status_opts, default=status_opts)

filtered = activities[
    activities["sector"].isin(f_sector)
    & activities["upazila"].isin(f_upazila)
    & activities["partner_org"].isin(f_partner)
    & activities["status"].isin(f_status)
]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Activities", len(filtered))
col2.metric("Partner organizations", filtered["partner_org"].nunique())
col3.metric("Sites covered", filtered["site_id"].nunique())
col4.metric("Sectors active", filtered["sector"].nunique())

st.write("")
map_col, chart_col = st.columns([2, 1])

with map_col:
    st.subheader("Where: Activities by Site")
    site_activity_counts = (
        filtered.groupby("site_id").size().rename("activity_count").reset_index()
    )
    map_df = sites.merge(site_activity_counts, on="site_id", how="inner")

    # Upazila-level totals for the choropleth fill -- every real boundary
    # polygon gets a row (0 if nothing matched the current filters), joined
    # on P-code so the fill always lands on the right polygon.
    upazila_totals = (
        filtered.groupby("official_adm3_pcode").size().rename("activity_count").reset_index()
    )
    all_pcodes = crosswalk[["official_adm3_pcode", "official_adm3_name"]].drop_duplicates()
    choropleth_df = all_pcodes.merge(upazila_totals, on="official_adm3_pcode", how="left")
    choropleth_df["activity_count"] = choropleth_df["activity_count"].fillna(0)

    fig_map = go.Figure()
    fig_map.add_trace(go.Choroplethmapbox(
        geojson=boundaries_geojson, locations=choropleth_df["official_adm3_pcode"],
        z=choropleth_df["activity_count"], featureidkey="properties.adm3_pcode",
        colorscale=SEQUENTIAL_BLUE, marker_opacity=0.55, marker_line_width=1.5,
        marker_line_color=INK_MUTED,
        text=choropleth_df["official_adm3_name"], hovertemplate="%{text}<br>Activities: %{z}<extra></extra>",
        colorbar=dict(title="Activities<br>(by upazila)", tickfont=dict(color=INK_SECONDARY), title_font=dict(color=INK_SECONDARY)),
    ))
    if not map_df.empty:
        fig_map.add_trace(go.Scattermapbox(
            lat=map_df["lat"], lon=map_df["lon"],
            mode="markers",
            marker=dict(size=map_df["activity_count"] * 6 + 10, color=CATEGORICAL_2, opacity=0.9),
            text=map_df["metadata/site_name"] + "<br>Activities: " + map_df["activity_count"].astype(str),
            hovertemplate="%{text}<extra></extra>",
        ))
    fig_map.update_layout(
        mapbox=dict(style="open-street-map", zoom=8.2, center=dict(lat=21.3, lon=92.15)),
        margin=dict(l=0, r=0, t=0, b=0), height=480,
        font=CHART_FONT, showlegend=False,
        paper_bgcolor=SURFACE,
    )
    st.plotly_chart(fig_map, use_container_width=True)
    if map_df.empty:
        st.info("No activities match the current filters -- showing upazila boundaries only.")

with chart_col:
    st.subheader("What: By Sector")
    if not filtered.empty:
        sector_counts = filtered["sector"].value_counts().reset_index()
        sector_counts.columns = ["sector", "count"]
        fig_bar = px.bar(sector_counts, x="count", y="sector", orientation="h")
        fig_bar.update_traces(marker_color=CATEGORICAL_1, marker_line_width=0)
        style_chart(fig_bar, height=260)
        fig_bar.update_yaxes(title=None)
        fig_bar.update_xaxes(title="Count")
        st.plotly_chart(fig_bar, use_container_width=True)

        st.subheader("Status")
        status_counts = filtered["status"].value_counts().reset_index()
        status_counts.columns = ["status", "count"]
        status_counts["status"] = pd.Categorical(status_counts["status"], categories=STATUS_ORDER, ordered=True)
        status_counts = status_counts.sort_values("status")
        fig_pie = go.Figure(
            data=[go.Pie(
                labels=status_counts["status"], values=status_counts["count"], hole=0.55,
                marker=dict(colors=[STATUS_COLORS[s] for s in status_counts["status"]], line=dict(color=SURFACE, width=2)),
                textfont=dict(color=INK_PRIMARY),
            )]
        )
        style_chart(fig_pie, height=240, legend=True)
        st.plotly_chart(fig_pie, use_container_width=True)

st.subheader("Activity List")
st.dataframe(
    filtered[["activity_id", "partner_org", "sector", "site_name", "upazila", "status", "start_date"]]
    .sort_values("start_date", ascending=False),
    use_container_width=True,
    hide_index=True,
)
