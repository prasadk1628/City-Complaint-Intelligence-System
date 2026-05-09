import streamlit as st
import pandas as pd
import plotly.express as px

from utils.config import (
    TEAL,
    AMBER,
    RED,
    BLUE,
    PURPLE,
    PLOTLY_BASE,
)


def render_overview(
    fdf,
    metrics
):

    total = metrics["total"]
    resolved = metrics["resolved"]
    open_cnt = metrics["open_cnt"]
    res_rate = metrics["res_rate"]
    open_rate = metrics["open_rate"]
    peak_month = metrics["peak_month"]

    st.title("📊 Overview")

    # ========================================================
    # KPI ROW
    # ========================================================

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "Total Complaints",
        f"{total:,}"
    )

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

    k4.metric(
        "Peak Month",
        str(peak_month)
    )

    st.divider()

    # ========================================================
    # MAIN CHARTS
    # ========================================================

    col_l, col_r = st.columns([1, 2])

    # --------------------------------------------------------
    # STATUS DONUT
    # --------------------------------------------------------

    with col_l:

        st.subheader("Status breakdown")

        status_counts = (
            fdf["complaint_status_title"]
            .value_counts()
            .reset_index()
        )

        status_counts.columns = [
            "Status",
            "Count"
        ]

        color_map = {
            "Resolved": TEAL,
            "Open": AMBER,
            "Pending": PURPLE,
            "Closed": BLUE,
            "Rejected": RED,
        }

        fig_donut = px.pie(
            status_counts,
            names="Status",
            values="Count",
            hole=0.65,
            color="Status",
            color_discrete_map=color_map,
        )

        fig_donut.update_traces(
            textposition="outside",
            textinfo="percent+label"
        )

        fig_donut.update_layout(
            **PLOTLY_BASE,
            height=320,
            showlegend=False
        )

        st.plotly_chart(
            fig_donut,
            use_container_width=True
        )

    # --------------------------------------------------------
    # MONTHLY TREND
    # --------------------------------------------------------

    with col_r:

        st.subheader(
            "Monthly complaint pattern"
        )

        monthly_agg = (
            fdf.assign(
                month_num=fdf["created_at"]
                .dt.month
            )
            .groupby("month_num")
            .size()
            .reset_index(name="count")
        )

        month_names = [
            "Jan","Feb","Mar","Apr","May","Jun",
            "Jul","Aug","Sep","Oct","Nov","Dec"
        ]

        monthly_agg["month_name"] = (
            monthly_agg["month_num"]
            .apply(
                lambda m: month_names[m - 1]
            )
        )

        fig_mon = px.bar(
            monthly_agg,
            x="month_name",
            y="count",
            color="count",
            color_continuous_scale=[
                [0, "rgba(55,138,221,0.35)"],
                [0.6, AMBER],
                [1.0, RED]
            ],
            labels={
                "month_name": "",
                "count": "Complaints"
            },
        )

        fig_mon.update_layout(
            **PLOTLY_BASE,
            height=380,
            coloraxis_showscale=False,
        )

        fig_mon.update_xaxes(
            tickmode="array",
            tickvals=month_names,
            ticktext=month_names
        )

        st.plotly_chart(
            fig_mon,
            use_container_width=True
        )

    st.divider()

    # ========================================================
    # SYSTEM VERDICT
    # ========================================================

    st.subheader("🧠 System Verdict")

    if res_rate < 40:

        st.error(
            f"🚨 **Critical performance** — "
            f"resolution rate of {res_rate:.1f}% "
            "indicates severe inefficiency. "
            "Immediate structural intervention required."
        )

    elif res_rate < 70:

        st.warning(
            f"⚠️ **Moderate performance** — "
            f"{res_rate:.1f}% resolution is "
            "below the 70% target. "
            "Targeted agency and ward "
            "improvements can close the gap."
        )

    else:

        st.success(
            f"✅ **Good performance** — "
            f"resolution rate of {res_rate:.1f}% "
            "meets target. Maintain quality "
            "and focus on edge-case categories."
        )