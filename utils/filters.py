import pandas as pd


def apply_filters(
    df,
    sel_year,
    sel_ward,
    sel_agency
):

    fdf = df.copy()

    if sel_year != "All":

        fdf = fdf[
            fdf["year"] == sel_year
        ]

    if sel_ward != "All":

        fdf = fdf[
            fdf["ward_title"] == sel_ward
        ]

    if sel_agency != "All":

        fdf = fdf[
            fdf["civic_agency_title"]
            == sel_agency
        ]

    ward_df = fdf[
        fdf["ward_title"] != "Other"
    ]

    return fdf, ward_df


def compute_metrics(fdf):

    total = len(fdf)

    resolved = (
        fdf["is_resolved"]
        .sum()
    )

    open_cnt = (
        fdf["is_open"]
        .sum()
    )

    res_rate = (
        (resolved / total) * 100
        if total > 0 else 0
    )

    open_rate = (
        (open_cnt / total) * 100
        if total > 0 else 0
    )

    monthly = (
        fdf.groupby(
            fdf["created_at"]
            .dt.to_period("M")
        )
        .size()
    )

    peak_month = (
        monthly.idxmax()
        if len(monthly) > 0
        else "N/A"
    )

    metrics = {

        "total":
            total,

        "resolved":
            resolved,

        "open_cnt":
            open_cnt,

        "res_rate":
            res_rate,

        "open_rate":
            open_rate,

        "monthly":
            monthly,

        "peak_month":
            peak_month,
    }

    return metrics