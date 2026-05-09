import streamlit as st
import plotly.express as px

from utils.config import (
    TEAL,
    AMBER,
    RED,
    PURPLE,
    PLOTLY_BASE,
    hex_to_rgba,
)


def render_agencies(fdf):

    st.title("🏢 Agency Performance")

    # ========================================================
    # AGENCY PERFORMANCE TABLE
    # ========================================================

    agency_perf = (
        fdf.groupby("civic_agency_title")
        .agg(
            complaints=(
                "civic_agency_title",
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
            "resolution_rate",
            ascending=False
        )
    )

    # ========================================================
    # RESOLUTION RANKING
    # ========================================================

    st.subheader(
        "Resolution rate ranking"
    )

    top_ag = (
        agency_perf
        .head(12)
        .reset_index()
    )

    fig_ag = px.bar(
        top_ag.sort_values(
            "resolution_rate"
        ),
        x="resolution_rate",
        y="civic_agency_title",
        orientation="h",
        color="resolution_rate",
        color_continuous_scale=[
            [0, RED],
            [0.5, AMBER],
            [1.0, TEAL]
        ],
        range_color=[0, 100],
        text=(
            top_ag
            .sort_values("resolution_rate")
            ["resolution_rate"]
            .astype(str) + "%"
        ),
        labels={
            "resolution_rate":
                "Resolution %",

            "civic_agency_title":
                "",
        },
    )

    fig_ag.update_traces(
        textposition="outside"
    )

    fig_ag.add_vline(
        x=70,
        line_dash="dash",
        line_color="#888",
        annotation_text="70% target",
        annotation_position="top right"
    )

    fig_ag.update_layout(
        **PLOTLY_BASE,
        height=480,
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig_ag,
        use_container_width=True
    )

    st.divider()

    # ========================================================
    # LOWER PANELS
    # ========================================================

    col_l, col_r = st.columns(2)

    # --------------------------------------------------------
    # VOLUME CHART
    # --------------------------------------------------------

    with col_l:

        st.subheader(
            "Complaint volume by agency"
        )

        vol = (
            agency_perf
            .sort_values(
                "complaints",
                ascending=False
            )
            .head(10)
        )

        fig_vol = px.bar(
            vol.sort_values(
                "complaints"
            ).reset_index(),
            x="complaints",
            y="civic_agency_title",
            orientation="h",
            color="complaints",
            color_continuous_scale=[
                [0, hex_to_rgba(PURPLE, 0.35)],
                [1.0, PURPLE]
            ],
            text="complaints",
            labels={
                "complaints":
                    "Complaints",

                "civic_agency_title":
                    "",
            },
        )

        fig_vol.update_traces(
            textposition="outside"
        )

        fig_vol.update_layout(
            **PLOTLY_BASE,
            height=380,
            coloraxis_showscale=False
        )

        st.plotly_chart(
            fig_vol,
            use_container_width=True
        )

    # --------------------------------------------------------
    # TABLE
    # --------------------------------------------------------

    with col_r:

        st.subheader(
            "Agency data table"
        )

        display_ag = (
            agency_perf
            .reset_index()
            .rename(columns={
                "civic_agency_title":
                    "Agency",

                "complaints":
                    "Complaints",

                "resolution_rate":
                    "Resolution %",
            })
        )

        st.dataframe(
            display_ag,
            use_container_width=True,
            height=380
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