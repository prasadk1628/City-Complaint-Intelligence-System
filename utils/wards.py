import streamlit as st
import plotly.express as px

from utils.config import (
    TEAL,
    AMBER,
    RED,
    PLOTLY_BASE,
)


def render_wards(
    fdf,
    ward_df,
    metrics,
    sel_ward
):

    total = metrics["total"]

    st.title("🏘️ Ward Intelligence")

    # ========================================================
    # WARD STATS
    # ========================================================

    ward_stats = (
        ward_df.groupby("ward_title")
        .agg(
            complaints=(
                "ward_title",
                "count"
            ),

            resolution_rate=(
                "is_resolved",
                lambda x: round(
                    x.mean() * 100,
                    1
                )
            ),
        )
        .sort_values(
            "complaints",
            ascending=False
        )
    )

    col_l, col_r = st.columns(2)

    # --------------------------------------------------------
    # TOP WARDS
    # --------------------------------------------------------

    with col_l:

        st.subheader(
            "Top 10 wards by volume"
        )

        top10 = (
            ward_stats
            .head(10)
            .sort_values("complaints")
        )

        fig_w = px.bar(
            top10,
            x="complaints",
            y=top10.index,
            orientation="h",
            color="resolution_rate",
            color_continuous_scale=[
                [0, RED],
                [0.5, AMBER],
                [1.0, TEAL]
            ],
            range_color=[0, 100],
            text="complaints",
            labels={
                "complaints": "Complaints",
                "y": "",
            },
        )

        fig_w.update_traces(
            textposition="outside"
        )

        fig_w.update_layout(
            **PLOTLY_BASE,
            height=420,
            coloraxis_colorbar=dict(
                title="Res. %",
                tickfont=dict(size=9)
            )
        )

        st.plotly_chart(
            fig_w,
            use_container_width=True
        )

    # --------------------------------------------------------
    # RESOLUTION RATE
    # --------------------------------------------------------

    with col_r:

        st.subheader(
            "Resolution rate by ward"
        )

        top10_res = (
            ward_stats
            .sort_values("resolution_rate")
            .head(10)
        )

        fig_r = px.bar(
            top10_res,
            x="resolution_rate",
            y=top10_res.index,
            orientation="h",
            color="resolution_rate",
            color_continuous_scale=[
                [0, RED],
                [0.5, AMBER],
                [1.0, TEAL]
            ],
            range_color=[0, 100],
            text=(
                top10_res["resolution_rate"]
                .astype(str) + "%"
            ),
            labels={
                "resolution_rate":
                    "Resolution %",
                "y":
                    "",
            },
        )

        fig_r.update_traces(
            textposition="outside"
        )

        fig_r.update_layout(
            **PLOTLY_BASE,
            height=420,
            coloraxis_showscale=False
        )

        st.plotly_chart(
            fig_r,
            use_container_width=True
        )

    st.divider()

    # ========================================================
    # QUADRANT ANALYSIS
    # ========================================================

    st.subheader(
        "Ward performance quadrant — "
        "volume vs resolution"
    )

    st.caption(
        "Wards in the bottom-left are "
        "high-risk: many complaints AND "
        "low resolution. Bubble size = "
        "complaint volume."
    )

    top20 = (
        ward_stats
        .head(20)
        .reset_index()
    )

    fig_s = px.scatter(
        top20,
        x="complaints",
        y="resolution_rate",
        text="ward_title",
        size="complaints",
        size_max=28,
        color="resolution_rate",
        color_continuous_scale=[
            [0, RED],
            [0.5, AMBER],
            [1.0, TEAL]
        ],
        range_color=[0, 100],
        labels={
            "complaints":
                "Complaint Volume",

            "resolution_rate":
                "Resolution Rate (%)"
        },
    )

    fig_s.update_traces(
        textposition="top center",
        textfont_size=9
    )

    fig_s.add_hline(
        y=70,
        line_dash="dash",
        line_color="#888",
        annotation_text="70% target",
        annotation_position="top right"
    )

    fig_s.update_layout(
        **PLOTLY_BASE,
        height=460,
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig_s,
        use_container_width=True
    )

    st.divider()

    # ========================================================
    # PRIORITY WARDS
    # ========================================================

    st.subheader(
        "Top 5 priority wards"
    )

    worst = (
        ward_stats[
            ward_stats["resolution_rate"] < 65
        ]
        .head(5)
        .reset_index()
    )

    worst.columns = [
        "Ward",
        "Complaints",
        "Resolution %"
    ]

    st.dataframe(
        worst,
        use_container_width=True
    )

    # ========================================================
    # SELECTED WARD INSIGHT
    # ========================================================

    if sel_ward != "All":

        st.subheader(
            f"Main issue in {sel_ward}"
        )

        top_issue = (
            fdf["category_title"]
            .value_counts()
            .head(1)
        )

        st.info(
            f"**{top_issue.index[0]}** — "
            f"{top_issue.values[0]:,} complaints "
            f"({top_issue.values[0]/total*100:.1f}% "
            "of all filtered complaints)"
        )