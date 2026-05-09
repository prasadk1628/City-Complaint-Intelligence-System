import streamlit as st
import folium

from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

from utils.data_loader import prepare_map_data


def render_spatial_analysis(fdf):

    st.title("🗺️ Spatial Analysis")

    # ========================================================
    # MAP DATA
    # ========================================================

    map_data = prepare_map_data(fdf)

    if len(map_data) == 0:

        st.warning(
            "No valid coordinate data available."
        )

        return

    st.subheader("Complaint Hotspots")

    st.caption(
        f"Showing {len(map_data):,} "
        "geolocated complaints."
    )

    # ========================================================
    # BENGALURU-FOCUSED MAP
    # ========================================================

    m = folium.Map(
        location=[12.9716, 77.5946],
        zoom_start=11,
        min_zoom=10,
        max_zoom=14,
        tiles="CartoDB dark_matter",
        prefer_canvas=True,
        control_scale=False,
        zoom_control=True,
    )

    # Restrict viewport to Bengaluru

    m.fit_bounds([
        [12.71, 77.43],
        [13.18, 77.81]
    ])

    # ========================================================
    # PERFORMANCE OPTIMIZATION
    # ========================================================

    sample_data = map_data.sample(
        min(700, len(map_data)),
        random_state=42
    )

    # ========================================================
    # STATUS COLORS
    # ========================================================

    color_map = {

        "Resolved":
            "#1D9E75",

        "Open":
            "#EF9F27",

        "Pending":
            "#7F77DD",

        "Closed":
            "#378ADD",

        "Rejected":
            "#E24B4A",
    }

    # ========================================================
    # MARKER CLUSTER
    # ========================================================

    marker_cluster = (
        MarkerCluster()
        .add_to(m)
    )

    for _, row in sample_data.iterrows():

        status = row.get(
            "complaint_status_title",
            "Open"
        )

        folium.CircleMarker(

            location=[
                row["latitude"],
                row["longitude"]
            ],

            radius=4,

            color=color_map.get(
                status,
                "#EF9F27"
            ),

            fill=True,

            fill_opacity=0.75,

            weight=1,

            tooltip=(
                f"{row['category_title']} | "
                f"{status}"
            )

        ).add_to(marker_cluster)

    # ========================================================
    # RENDER MAP
    # ========================================================

    st_folium(
        m,
        width=1400,
        height=550,
        returned_objects=[]
    )

    st.divider()

    # ========================================================
    # HOTSPOT TABLE
    # ========================================================

    st.subheader(
        "Top Hotspot Wards"
    )

    hotspot = (
        map_data.groupby("ward_title")
        .size()
        .reset_index(name="complaints")
        .sort_values(
            "complaints",
            ascending=False
        )
        .head(10)
    )

    hotspot.index = hotspot.index + 1

    st.dataframe(
        hotspot,
        use_container_width=True
    )

    st.divider()

    # ========================================================
    # SPATIAL INSIGHTS
    # ========================================================

    st.subheader(
        "🧠 Spatial Insights"
    )

    top_ward = hotspot.iloc[0]["ward_title"]

    top_count = hotspot.iloc[0]["complaints"]

    st.warning(
        f"⚠️ **{top_ward}** shows the "
        f"highest complaint concentration "
        f"with **{top_count:,} complaints**."
    )

    st.info(
        "Clustered complaint zones indicate "
        "probable infrastructure stress "
        "regions requiring priority "
        "intervention."
    )

    st.success(
        "Marker clustering and Bengaluru-"
        "focused viewport optimization "
        "significantly improve dashboard "
        "performance and readability."
    )