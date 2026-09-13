"""4W/5W operational dashboard -- Who's doing What, Where, When (for Whom).

Follows the standard cluster-coordination 4W/5W template structure: a
partner/sector/site/status activity table, map + table views, and summary
counts. Built entirely from this repo's synthetic/fictional data --
Phase R1's synthetic site assessments and a fictional partner-activity list
(scripts/generate_4w_data.py). No real organization, site, or population
data.

Run: streamlit run dashboard/app.py
"""

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="4W Dashboard -- Rapid Assessment Sites", layout="wide")

SITES_CSV = "data/synthetic_site_assessments.csv"
ACTIVITIES_CSV = "data/fictional_4w_activities.csv"


@st.cache_data
def load_data():
    sites = pd.read_csv(SITES_CSV)
    activities = pd.read_csv(ACTIVITIES_CSV)
    gps = sites["location/gps_point"].str.split(" ", expand=True)
    sites["lat"] = gps[0].astype(float)
    sites["lon"] = gps[1].astype(float)
    return sites, activities


sites, activities = load_data()

st.title("4W Dashboard: Who's doing What, Where, When")
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
    status_opts = sorted(activities["status"].unique())

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

map_col, chart_col = st.columns([2, 1])

with map_col:
    st.subheader("Where: activities by site")
    site_activity_counts = (
        filtered.groupby("site_id").size().rename("activity_count").reset_index()
    )
    map_df = sites.merge(site_activity_counts, on="site_id", how="inner")
    if not map_df.empty:
        fig_map = px.scatter_mapbox(
            map_df, lat="lat", lon="lon", size="activity_count", color="activity_count",
            hover_name="metadata/site_name",
            hover_data={"lat": False, "lon": False, "location/upazila": True, "activity_count": True},
            color_continuous_scale="OrRd", zoom=8.2, height=480,
        )
        fig_map.update_layout(mapbox_style="open-street-map", margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("No activities match the current filters.")

with chart_col:
    st.subheader("What: by sector")
    if not filtered.empty:
        sector_counts = filtered["sector"].value_counts().reset_index()
        sector_counts.columns = ["sector", "count"]
        fig_bar = px.bar(sector_counts, x="count", y="sector", orientation="h")
        fig_bar.update_layout(height=250, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig_bar, use_container_width=True)

        st.subheader("Status")
        status_counts = filtered["status"].value_counts().reset_index()
        status_counts.columns = ["status", "count"]
        fig_pie = px.pie(status_counts, names="status", values="count", hole=0.5)
        fig_pie.update_layout(height=220, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig_pie, use_container_width=True)

st.subheader("Activity list")
st.dataframe(
    filtered[["activity_id", "partner_org", "sector", "site_name", "upazila", "status", "start_date"]]
    .sort_values("start_date", ascending=False),
    use_container_width=True,
    hide_index=True,
)
