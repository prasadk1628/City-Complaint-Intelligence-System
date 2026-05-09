import streamlit as st

from utils.data_loader import load_data

from utils.filters import (
    apply_filters,
    compute_metrics,
)

from utils.overview import render_overview
from utils.complaints import render_complaints
from utils.wards import render_wards
from utils.agencies import render_agencies
from utils.maps import render_spatial_analysis
from utils.insights import render_insights
# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="City Complaint Intelligence",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# LOAD DATA
# ============================================================

df = load_data()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("### 🏙️ City Intelligence")
    st.caption("Urban Complaint Analytics")
    st.divider()

    page = st.radio(
        "Navigate",
        options=[
            "📊 Overview",
            "📋 Complaints",
            "🏘️ Ward Intelligence",
            "🏢 Agency Performance",
            "🗺️ Spatial Analysis",
            "🧠 Insights",
        ],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("**Filters**")

    year_opts = ["All"] + sorted(
        df["year"].unique().tolist()
    )

    sel_year = st.selectbox(
        "Year",
        year_opts
    )

    ward_opts = ["All"] + sorted(
        df["ward_title"].unique().tolist()
    )

    sel_ward = st.selectbox(
        "Ward",
        ward_opts
    )

    agency_opts = ["All"] + sorted(
        df["civic_agency_title"].unique().tolist()
    )

    sel_agency = st.selectbox(
        "Agency",
        agency_opts
    )

    st.divider()

    st.caption(
        f"Last data: `{df['created_at'].max().date()}`"
    )

# ============================================================
# APPLY FILTERS
# ============================================================

fdf, ward_df = apply_filters(
    df,
    sel_year,
    sel_ward,
    sel_agency
)

metrics = compute_metrics(fdf)

# ============================================================
# PAGE ROUTING
# ============================================================

if page == "📊 Overview":

    render_overview(
        fdf,
        metrics
    )

elif page == "📋 Complaints":

    render_complaints(
        fdf
    )

elif page == "🏘️ Ward Intelligence":

    render_wards(
        fdf,
        ward_df,
        metrics,
        sel_ward
    )

elif page == "🏢 Agency Performance":

    render_agencies(
        fdf
    )

elif page == "🗺️ Spatial Analysis":

    render_spatial_analysis(
        fdf
    )

elif page == "🧠 Insights":

    render_insights(
        fdf,
        ward_df,
        metrics
    )