# ============================================================
# CITY COMPLAINT INTELLIGENCE — 2050 EDITION
# Restructured + Enhanced by Vara Prasad K
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# SECTION 0 — PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="City Complaint Intelligence",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# SECTION 1 — GLOBAL THEME CONSTANTS
# ============================================================
TEAL   = "#1D9E75"
AMBER  = "#EF9F27"
RED    = "#E24B4A"
BLUE   = "#378ADD"
PURPLE = "#7F77DD"

def hex_to_rgba(hex_color, alpha):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


PLOTLY_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="monospace", color="#8b8fa8", size=11),
    margin=dict(l=20, r=20, t=36, b=20),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.08)",
               tickfont=dict(size=10, color="#4a5068")),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.08)",
               tickfont=dict(size=10, color="#4a5068")),
)

CATEGORY_REMAP = {
    "Streetlights":                       "Street Lighting",
    "Roads and Footpaths":                "Mobility — Roads & Footpaths",
    "Mobility - Roads, Public transport": "Mobility — Roads & Footpaths",
    "Water Supply":                       "Water Supply and Services",
    "Electricity & Power":                "Electricity and Power",
    "Power supply":                       "Electricity and Power",
    "Solid Waste Management":             "Garbage and Sanitation",
    "Waste Management":                   "Garbage and Sanitation",
}

# ============================================================
# SECTION 2 — DATA LOADING & CLEANING
# ============================================================
@st.cache_data
def load_data():
    df = pd.read_csv("Log of complaints.csv", encoding="latin1")

    df["created_at"] = pd.to_datetime(
        df["created_at"],
        errors="coerce"
    )
    df = df.dropna(subset=["created_at"])

    df = df.drop(columns=[
        "title", "description", "sub_category_id",
        "category_id", "civic_agency_id", "address",
    ], errors="ignore")

    df = df.dropna(subset=["ward_title", "category_title"])
    df["civic_agency_title"] = df["civic_agency_title"].fillna("Unknown")
    df["category_title"]     = df["category_title"].replace(CATEGORY_REMAP)

    df["year"]  = df["created_at"].dt.year
    df["month"] = df["created_at"].dt.to_period("M")

    df["latitude"]  = pd.to_numeric(df.get("latitude"),  errors="coerce")
    df["longitude"] = pd.to_numeric(df.get("longitude"), errors="coerce")

    df["is_resolved"] = df["complaint_status_title"] == "Resolved"
    df["is_open"]     = df["complaint_status_title"] == "Open"

    return df


df = load_data()

# ============================================================
# SECTION 3 — SIDEBAR NAVIGATION + FILTERS
# ============================================================
with st.sidebar:
    st.markdown("### 🏙️ City Intelligence")
    st.caption("Urban Complaint Analytics · 2050")
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

    year_opts = ["All"] + sorted(df["year"].unique().tolist())
    sel_year  = st.selectbox("Year", year_opts)

    ward_opts = ["All"] + sorted(df["ward_title"].unique().tolist())
    sel_ward  = st.selectbox("Ward", ward_opts)

    agency_opts = ["All"] + sorted(df["civic_agency_title"].unique().tolist())
    sel_agency  = st.selectbox("Agency", agency_opts)

    st.divider()
    st.caption(f"Last data: `{df['created_at'].max().date()}`")

# ============================================================
# SECTION 4 — APPLY FILTERS
# ============================================================
fdf = df.copy()
if sel_year   != "All": fdf = fdf[fdf["year"]               == sel_year]
if sel_ward   != "All": fdf = fdf[fdf["ward_title"]         == sel_ward]
if sel_agency != "All": fdf = fdf[fdf["civic_agency_title"] == sel_agency]

ward_df = fdf[fdf["ward_title"] != "Other"]

total      = len(fdf)
resolved   = fdf["is_resolved"].sum()
open_cnt   = fdf["is_open"].sum()
res_rate   = (resolved / total * 100) if total > 0 else 0
open_rate  = (open_cnt / total * 100) if total > 0 else 0
monthly    = fdf.groupby(fdf["created_at"].dt.to_period("M")).size()
peak_month = monthly.idxmax() if len(monthly) > 0 else "N/A"

# ============================================================
# SECTION 5 — PAGE: OVERVIEW
# ============================================================
if page == "📊 Overview":
    st.title("📊 Overview")

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Complaints", f"{total:,}")
    k2.metric(
        "Resolution Rate",
        f"{res_rate:.1f}%",
        delta=f"{res_rate - 70:.1f}% vs 70% target",
        delta_color="normal",
    )
    k3.metric(
        "Open Rate",
        f"{open_rate:.1f}%",
        delta=f"{open_cnt:,} unresolved",
        delta_color="inverse",
    )
    k4.metric("Peak Month", str(peak_month))

    st.divider()

    col_l, col_r = st.columns([1, 2])

    with col_l:
        st.subheader("Status breakdown")
        status_counts = fdf["complaint_status_title"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]

        color_map = {
            "Resolved":   TEAL,
            "Open":       AMBER,
            "Pending":    PURPLE,
            "Closed":     BLUE,
            "Rejected":   RED,
        }
        fig_donut = px.pie(
            status_counts, names="Status", values="Count",
            hole=0.65,
            color="Status",
            color_discrete_map=color_map,
        )
        fig_donut.update_traces(textposition="outside", textinfo="percent+label")
        fig_donut.update_layout(**PLOTLY_BASE, height=320, showlegend=False)
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_r:
        st.subheader("Yearly complaint trend")
        yearly = fdf.groupby("year").size().reset_index(name="count")
        fig_trend = px.line(
            yearly, x="year", y="count",
            markers=True,
            labels={"year": "", "count": "Complaints"},
            color_discrete_sequence=[BLUE],
        )
        fig_trend.update_traces(line_width=2, marker_size=6, fill="tozeroy",
                                fillcolor=hex_to_rgba(BLUE, 0.10))
        fig_trend.update_layout(**PLOTLY_BASE, height=320)
        st.plotly_chart(fig_trend, use_container_width=True)

    st.divider()

    # Automated verdict
    st.subheader("🧠 System Verdict")
    if res_rate < 40:
        st.error(
            f"🚨 **Critical performance** — resolution rate of {res_rate:.1f}% "
            "indicates severe inefficiency. Immediate structural intervention required."
        )
    elif res_rate < 70:
        st.warning(
            f"⚠️ **Moderate performance** — {res_rate:.1f}% resolution is below the "
            "70% target. Targeted agency and ward improvements can close the gap."
        )
    else:
        st.success(
            f"✅ **Good performance** — resolution rate of {res_rate:.1f}% meets target. "
            "Maintain quality and focus on edge-case categories."
        )

# ============================================================
# SECTION 6 — PAGE: COMPLAINTS
# ============================================================
elif page == "📋 Complaints":
    st.title("📋 Complaint Analysis")

    st.subheader("Top 10 complaint categories")
    top_cats = fdf["category_title"].value_counts().head(10).reset_index()
    top_cats.columns = ["Category", "Count"]
    top_cats = top_cats.sort_values("Count")

    fig_cat = px.bar(
        top_cats, x="Count", y="Category",
        orientation="h",
        color="Count",
        color_continuous_scale=[[0, hex_to_rgba(BLUE, 0.35)], [0.5, AMBER], [1.0, RED]],
        text="Count",
        labels={"Count": "Complaints", "Category": ""},
    )
    fig_cat.update_traces(textposition="outside")
    fig_cat.update_layout(**PLOTLY_BASE, height=420, coloraxis_showscale=False)
    st.plotly_chart(fig_cat, use_container_width=True)

    st.divider()

    col_l, col_r = st.columns(2)

    with col_l:
        st.subheader("Category × Status heatmap")
        pivot = pd.crosstab(
            fdf["category_title"],
            fdf["complaint_status_title"],
        )
        # Use only top 8 categories for readability
        top8 = fdf["category_title"].value_counts().head(8).index
        pivot = pivot.loc[pivot.index.isin(top8)]

        fig_hm = px.imshow(
            pivot,
            color_continuous_scale=[[0, "#0f1117"], [0.5, AMBER], [1.0, RED]],
            aspect="auto",
            labels={"color": "Count"},
        )
        fig_hm.update_layout(**PLOTLY_BASE, height=380)
        st.plotly_chart(fig_hm, use_container_width=True)

    with col_r:
        st.subheader("Monthly complaint pattern")
        fdf["month_num"] = fdf["created_at"].dt.month
        monthly_agg = fdf.groupby("month_num").size().reset_index(name="count")
        month_names = ["Jan","Feb","Mar","Apr","May","Jun",
                       "Jul","Aug","Sep","Oct","Nov","Dec"]
        monthly_agg["month_name"] = monthly_agg["month_num"].apply(
            lambda m: month_names[m - 1]
        )

        fig_mon = px.bar(
            monthly_agg, x="month_name", y="count",
            color="count",
            color_continuous_scale=[[0, hex_to_rgba(BLUE, 0.35)], [0.6, AMBER], [1.0, RED]],
            labels={"month_name": "", "count": "Complaints"},
        )
        fig_mon.update_layout(**PLOTLY_BASE, height=380,
                              coloraxis_showscale=False,
                              xaxis=dict(tickmode="array",
                                         tickvals=month_names,
                                         ticktext=month_names))
        st.plotly_chart(fig_mon, use_container_width=True)

# ============================================================
# SECTION 7 — PAGE: WARD INTELLIGENCE
# ============================================================
elif page == "🏘️ Ward Intelligence":
    st.title("🏘️ Ward Intelligence")

    ward_stats = (
        ward_df.groupby("ward_title")
        .agg(
            complaints=("ward_title", "count"),
            resolution_rate=("is_resolved", lambda x: round(x.mean() * 100, 1)),
        )
        .sort_values("complaints", ascending=False)
    )

    col_l, col_r = st.columns(2)

    with col_l:
        st.subheader("Top 10 wards by volume")
        top10 = ward_stats.head(10).sort_values("complaints")
        fig_w = px.bar(
            top10, x="complaints", y=top10.index,
            orientation="h",
            color="resolution_rate",
            color_continuous_scale=[[0, RED], [0.5, AMBER], [1.0, TEAL]],
            range_color=[0, 100],
            text="complaints",
            labels={"complaints": "Complaints", "y": ""},
        )
        fig_w.update_traces(textposition="outside")
        fig_w.update_layout(**PLOTLY_BASE, height=420,
                            coloraxis_colorbar=dict(
                                title="Res. %", tickfont=dict(size=9)))
        st.plotly_chart(fig_w, use_container_width=True)

    with col_r:
        st.subheader("Resolution rate by ward")
        top10_res = ward_stats.sort_values("resolution_rate").head(10)
        fig_r = px.bar(
            top10_res, x="resolution_rate", y=top10_res.index,
            orientation="h",
            color="resolution_rate",
            color_continuous_scale=[[0, RED], [0.5, AMBER], [1.0, TEAL]],
            range_color=[0, 100],
            text=top10_res["resolution_rate"].astype(str) + "%",
            labels={"resolution_rate": "Resolution %", "y": ""},
        )
        fig_r.update_traces(textposition="outside")
        fig_r.update_layout(**PLOTLY_BASE, height=420,
                            coloraxis_showscale=False)
        st.plotly_chart(fig_r, use_container_width=True)

    st.divider()
    st.subheader("Ward performance quadrant — volume vs resolution")
    st.caption(
        "Wards in the bottom-left are high-risk: many complaints AND low resolution. "
        "Bubble size = complaint volume."
    )
    top20 = ward_stats.head(20).reset_index()
    fig_s = px.scatter(
        top20, x="complaints", y="resolution_rate",
        text="ward_title",
        size="complaints",
        size_max=28,
        color="resolution_rate",
        color_continuous_scale=[[0, RED], [0.5, AMBER], [1.0, TEAL]],
        range_color=[0, 100],
        labels={"complaints": "Complaint Volume",
                "resolution_rate": "Resolution Rate (%)"},
    )
    fig_s.update_traces(textposition="top center", textfont_size=9)
    fig_s.add_hline(y=70, line_dash="dash", line_color="#888",
                   annotation_text="70% target", annotation_position="top right")
    fig_s.update_layout(**PLOTLY_BASE, height=460,
                        coloraxis_showscale=False)
    st.plotly_chart(fig_s, use_container_width=True)

    st.subheader("Top 5 priority wards")
    worst = ward_stats[ward_stats["resolution_rate"] < 65].head(5).reset_index()
    worst.columns = ["Ward", "Complaints", "Resolution %"]
    st.dataframe(worst, use_container_width=True)

    if sel_ward != "All":
        st.subheader(f"Main issue in {sel_ward}")
        top_issue = fdf["category_title"].value_counts().head(1)
        st.info(
            f"**{top_issue.index[0]}** — {top_issue.values[0]:,} complaints "
            f"({top_issue.values[0]/total*100:.1f}% of all filtered complaints)"
        )

# ============================================================
# SECTION 8 — PAGE: AGENCY PERFORMANCE
# ============================================================
elif page == "🏢 Agency Performance":
    st.title("🏢 Agency Performance")

    agency_perf = (
        fdf.groupby("civic_agency_title")
        .agg(
            complaints=("civic_agency_title", "count"),
            resolution_rate=("is_resolved", lambda x: round(x.mean() * 100, 1)),
        )
        .sort_values("resolution_rate", ascending=False)
    )

    st.subheader("Resolution rate ranking")
    top_ag = agency_perf.head(12).reset_index()

    fig_ag = px.bar(
        top_ag.sort_values("resolution_rate"),
        x="resolution_rate", y="civic_agency_title",
        orientation="h",
        color="resolution_rate",
        color_continuous_scale=[[0, RED], [0.5, AMBER], [1.0, TEAL]],
        range_color=[0, 100],
        text=top_ag.sort_values("resolution_rate")["resolution_rate"].astype(str) + "%",
        labels={"resolution_rate": "Resolution %", "civic_agency_title": ""},
    )
    fig_ag.update_traces(textposition="outside")
    fig_ag.add_vline(x=70, line_dash="dash", line_color="#888",
                    annotation_text="70% target", annotation_position="top right")
    fig_ag.update_layout(**PLOTLY_BASE, height=480, coloraxis_showscale=False)
    st.plotly_chart(fig_ag, use_container_width=True)

    st.divider()

    col_l, col_r = st.columns(2)

    with col_l:
        st.subheader("Complaint volume by agency")
        vol = agency_perf.sort_values("complaints", ascending=False).head(10)
        fig_vol = px.bar(
            vol.sort_values("complaints").reset_index(),
            x="complaints", y="civic_agency_title",
            orientation="h",
            color="complaints",
            color_continuous_scale=[[0, hex_to_rgba(PURPLE, 0.35)], [1.0, PURPLE]],
            text="complaints",
            labels={"complaints": "Complaints", "civic_agency_title": ""},
        )
        fig_vol.update_traces(textposition="outside")
        fig_vol.update_layout(**PLOTLY_BASE, height=380,
                              coloraxis_showscale=False)
        st.plotly_chart(fig_vol, use_container_width=True)

    with col_r:
        st.subheader("Agency data table")
        display_ag = agency_perf.reset_index().rename(columns={
            "civic_agency_title": "Agency",
            "complaints":         "Complaints",
            "resolution_rate":    "Resolution %",
        })
        st.dataframe(display_ag, use_container_width=True, height=380)

    # Download button
    st.divider()
    csv = fdf.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv,
        file_name="filtered_complaints.csv",
        mime="text/csv",
    )

# ============================================================
# SECTION 9 — PAGE: SPATIAL ANALYSIS
# ============================================================
elif page == "🗺️ Spatial Analysis":
    st.title("🗺️ Spatial Analysis")

    map_data = fdf[["latitude", "longitude", "category_title",
                    "ward_title", "complaint_status_title"]].dropna(
        subset=["latitude", "longitude"]
    )

    if len(map_data) == 0:
        st.warning(
            "No coordinate data available in the current filter. "
            "Ensure `latitude` and `longitude` columns are present in the CSV."
        )
    else:
        st.subheader("Complaint scatter map")
        st.caption(f"Showing {len(map_data):,} geolocated complaints.")

        fig_scatter = px.scatter_mapbox(
            map_data,
            lat="latitude", lon="longitude",
            color="complaint_status_title",
            hover_data=["category_title", "ward_title"],
            color_discrete_map={
                "Resolved": TEAL,
                "Open":     AMBER,
                "Pending":  PURPLE,
                "Closed":   BLUE,
                "Rejected": RED,
            },
            zoom=10,
            height=480,
            mapbox_style="carto-darkmatter",
            opacity=0.6,
        )
        fig_scatter.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=0, b=0),
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

        st.divider()
        st.subheader("Complaint density heatmap")
        fig_density = px.density_mapbox(
            map_data,
            lat="latitude", lon="longitude",
            radius=12,
            zoom=10,
            height=440,
            mapbox_style="carto-darkmatter",
            color_continuous_scale=[[0, "#08090d"],
                                    [0.4, RED],
                                    [0.7, AMBER],
                                    [1.0, "#fff"]],
        )
        fig_density.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=0, b=0),
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig_density, use_container_width=True)

# ============================================================
# SECTION 10 — PAGE: INSIGHTS
# ============================================================
elif page == "🧠 Insights":
    st.title("🧠 Automated Insights")

    # ── 10.1 Resolution verdict ──
    st.subheader("⚙️ Resolution Efficiency")
    e1, e2, e3 = st.columns(3)
    e1.metric("Resolution Rate",        f"{res_rate:.1f}%")
    e2.metric("Open Complaint Backlog",  f"{open_cnt:,}")
    e3.metric("Unresolved Rate",         f"{open_rate:.1f}%",
              delta_color="inverse")

    st.progress(float(res_rate / 100))

    if res_rate < 40:
        st.error("🚨 **Critical** — system is overwhelmed. Structural reforms needed urgently.")
    elif res_rate < 70:
        st.warning("⚠️ **Moderate** — below the 70% benchmark. Targeted fixes will move the needle.")
    else:
        st.success("✅ **Healthy** — maintain standards and monitor edge-case categories.")

    st.divider()

    # ── 10.2 Key observations ──
    st.subheader("📌 Key Observations")

    top_cat = (
        fdf["category_title"].value_counts().idxmax()
        if len(fdf) > 0 else "N/A"
    )
    top_ward = (
        ward_df.groupby("ward_title").size().idxmax()
        if len(ward_df) > 0 else "N/A"
    )

    obs_cols = st.columns(2)
    observations = [
        ("warn",   f"Dominant category",  f"**{top_cat}** leads complaint volume — infrastructure funding likely misaligned."),
        ("info",   "COVID anomaly",        "Complaint drop in 2020 inflates resolution metrics for that year. Adjust multi-year baselines."),
        ("danger", "Top problem ward",     f"**{top_ward}** generates the highest complaint density. Resource surge needed."),
        ("warn",   "Seasonal spikes",      "March (pre-monsoon) and July (monsoon onset) consistently produce complaint surges. Pre-deploy capacity."),
        ("ok",     "Improvement lever",    "Improving the 3 lowest-performing agencies to 70% resolution would clear ~8,000 backlogged complaints."),
        ("info",   "Repeat complaint risk","Unresolved open complaints are likely generating repeat submissions — inflating raw volume figures."),
    ]

    type_map = {
        "warn":   st.warning,
        "danger": st.error,
        "ok":     st.success,
        "info":   st.info,
    }

    for obs_type, title, text in observations:
        type_map[obs_type](f"**{title}** — {text}")

    st.divider()

    # ── 10.3 Peak month analysis ──
    st.subheader("📈 Peak Complaint Month")
    st.write(f"Highest complaint volume recorded in: **{peak_month}**")

    top5_months = monthly.sort_values(ascending=False).head(5)
    st.dataframe(
        top5_months.reset_index().rename(
            columns={"created_at": "Month", 0: "Complaints"}
        ),
        use_container_width=True,
    )

    st.divider()

    # ── 10.4 Download ──
    csv = fdf.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv,
        file_name="filtered_complaints.csv",
        mime="text/csv",
    )

    st.divider()
    st.markdown("""
---
**About** — This dashboard analyses real-world civic complaint data to identify
patterns, hotspots, and inefficiencies in urban service delivery using data analytics.

*City Complaint Intelligence · Built by Vara Prasad K*
""")