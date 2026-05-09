# ============================================================
# CONFIGURATION — THEME + GLOBAL CONSTANTS
# ============================================================

# ------------------------------------------------------------
# COLOR PALETTE
# ------------------------------------------------------------

TEAL   = "#1D9E75"
AMBER  = "#EF9F27"
RED    = "#E24B4A"
BLUE   = "#378ADD"
PURPLE = "#7F77DD"

# ------------------------------------------------------------
# HEX → RGBA CONVERTER
# ------------------------------------------------------------

def hex_to_rgba(hex_color, alpha):

    hex_color = hex_color.lstrip("#")

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return f"rgba({r},{g},{b},{alpha})"

# ------------------------------------------------------------
# PLOTLY GLOBAL THEME
# ------------------------------------------------------------

PLOTLY_BASE = dict(

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    font=dict(
        family="monospace",
        color="#8b8fa8",
        size=11
    ),

    margin=dict(
        l=20,
        r=20,
        t=36,
        b=20
    ),

    xaxis=dict(
        gridcolor="rgba(255,255,255,0.05)",
        linecolor="rgba(255,255,255,0.08)",
        tickfont=dict(
            size=10,
            color="#4a5068"
        )
    ),

    yaxis=dict(
        gridcolor="rgba(255,255,255,0.05)",
        linecolor="rgba(255,255,255,0.08)",
        tickfont=dict(
            size=10,
            color="#4a5068"
        )
    ),
)

# ------------------------------------------------------------
# CATEGORY STANDARDIZATION
# ------------------------------------------------------------

CATEGORY_REMAP = {

    "Streetlights":
        "Street Lighting",

    "Roads and Footpaths":
        "Mobility — Roads & Footpaths",

    "Mobility - Roads, Public transport":
        "Mobility — Roads & Footpaths",

    "Water Supply":
        "Water Supply and Services",

    "Electricity & Power":
        "Electricity and Power",

    "Power supply":
        "Electricity and Power",

    "Solid Waste Management":
        "Garbage and Sanitation",

    "Waste Management":
        "Garbage and Sanitation",
}