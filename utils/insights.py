import streamlit as st


def render_insights(
    fdf,
    ward_df,
    metrics
):

    total = metrics["total"]
    open_cnt = metrics["open_cnt"]
    res_rate = metrics["res_rate"]
    open_rate = metrics["open_rate"]
    monthly = metrics["monthly"]
    peak_month = metrics["peak_month"]

    st.title("🧠 Operational Insights")

    # ========================================================
    # RESOLUTION EFFICIENCY
    # ========================================================

    st.subheader(
        "⚙️ Resolution Efficiency"
    )

    e1, e2, e3 = st.columns(3)

    e1.metric(
        "Resolution Rate",
        f"{res_rate:.1f}%"
    )

    e2.metric(
        "Open Complaint Backlog",
        f"{open_cnt:,}"
    )

    e3.metric(
        "Unresolved Rate",
        f"{open_rate:.1f}%",
        delta_color="inverse"
    )

    st.progress(
        float(res_rate / 100)
    )

    if res_rate < 40:

        st.error(
            "🚨 **Critical** — system is "
            "overwhelmed. Structural reforms "
            "needed urgently."
        )

    elif res_rate < 70:

        st.warning(
            "⚠️ **Moderate** — below the "
            "70% benchmark. Targeted fixes "
            "will move the needle."
        )

    else:

        st.success(
            "✅ **Healthy** — maintain "
            "standards and monitor "
            "edge-case categories."
        )

    st.divider()

    # ========================================================
    # KEY OBSERVATIONS
    # ========================================================

    st.subheader("📌 Key Observations")

    top_cat = (
        fdf["category_title"]
        .value_counts()
        .idxmax()
        if len(fdf) > 0
        else "N/A"
    )

    top_ward = (
        ward_df.groupby("ward_title")
        .size()
        .idxmax()
        if len(ward_df) > 0
        else "N/A"
    )

    observations = [

        (
            "warning",
            "Dominant category",
            f"**{top_cat}** leads complaint "
            "volume — infrastructure funding "
            "likely misaligned."
        ),

        (
            "info",
            "COVID anomaly",
            "Complaint drop in 2020 inflates "
            "resolution metrics for that year. "
            "Adjust multi-year baselines."
        ),

        (
            "error",
            "Top problem ward",
            f"**{top_ward}** generates the "
            "highest complaint density. "
            "Resource surge needed."
        ),

        (
            "warning",
            "Seasonal spikes",
            "March and July consistently "
            "produce complaint surges. "
            "Pre-deploy operational capacity."
        ),

        (
            "success",
            "Improvement lever",
            "Improving the 3 lowest-performing "
            "agencies to 70% resolution could "
            "significantly reduce backlog."
        ),

        (
            "info",
            "Repeat complaint risk",
            "Unresolved complaints may be "
            "creating repeat submissions, "
            "inflating raw complaint volume."
        ),
    ]

    for obs_type, title, text in observations:

        getattr(st, obs_type)(
            f"**{title}** — {text}"
        )

    st.divider()

    # ========================================================
    # PEAK MONTH ANALYSIS
    # ========================================================

    st.subheader(
        "📈 Peak Complaint Month"
    )

    st.write(
        f"Highest complaint volume "
        f"recorded in: **{peak_month}**"
    )

    top5_months = (
        monthly
        .sort_values(ascending=False)
        .head(5)
    )

    st.dataframe(
        top5_months
        .reset_index()
        .rename(columns={
            "created_at": "Month",
            0: "Complaints"
        }),
        use_container_width=True,
    )

    st.divider()

    # ========================================================
    # DOWNLOAD
    # ========================================================

    csv = (
        fdf.to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv,
        file_name="filtered_complaints.csv",
        mime="text/csv",
    )

    st.divider()

    # ========================================================
    # ABOUT
    # ========================================================

    st.markdown("""
---
### About

This dashboard analyzes real-world civic complaint data to identify:

- operational inefficiencies
- spatial hotspots
- service gaps
- resolution performance

using data analytics and interactive visualization.

**City Complaint Intelligence · Built by Vara Prasad K**
""")