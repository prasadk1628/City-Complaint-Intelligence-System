import streamlit as st
import pandas as pd
import plotly.express as px

from utils.config import (
    AMBER,
    RED,
    BLUE,
    PLOTLY_BASE,
    hex_to_rgba,
)


def render_complaints(fdf):

    st.title("📋 Complaint Analysis")

    # ========================================================
    # TOP CATEGORIES
    # ========================================================

    st.subheader("Top 10 complaint categories")

    top_cats = (
        fdf["category_title"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_cats.columns = [
        "Category",
        "Count"
    ]

    top_cats = top_cats.sort_values(
        "Count"
    )

    fig_cat = px.bar(
        top_cats,
        x="Count",
        y="Category",
        orientation="h",
        color="Count",
        color_continuous_scale=[
            [0, hex_to_rgba(BLUE, 0.35)],
            [0.5, AMBER],
            [1.0, RED]
        ],
        text="Count",
        labels={
            "Count": "Complaints",
            "Category": "",
        },
    )

    fig_cat.update_traces(
        textposition="outside"
    )

    fig_cat.update_layout(
        **PLOTLY_BASE,
        height=420,
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig_cat,
        use_container_width=True
    )

    st.divider()

    # ========================================================
    # LOWER PANELS
    # ========================================================

    col_l, col_r = st.columns(2)

    # --------------------------------------------------------
    # HEATMAP
    # --------------------------------------------------------

    with col_l:

        st.subheader(
            "Category × Status heatmap"
        )

        pivot = pd.crosstab(
            fdf["category_title"],
            fdf["complaint_status_title"],
        )

        top8 = (
            fdf["category_title"]
            .value_counts()
            .head(8)
            .index
        )

        pivot = pivot.loc[
            pivot.index.isin(top8)
        ]

        fig_hm = px.imshow(
            pivot,
            color_continuous_scale=[
                [0, "#0f1117"],
                [0.5, AMBER],
                [1.0, RED]
            ],
            aspect="auto",
            labels={
                "color": "Count"
            },
        )

        fig_hm.update_layout(
            **PLOTLY_BASE,
            height=380
        )

        st.plotly_chart(
            fig_hm,
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