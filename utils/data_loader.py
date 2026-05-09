import streamlit as st
import pandas as pd

from utils.config import CATEGORY_REMAP


@st.cache_data
def load_data():

    df = pd.read_csv(
        "Log of complaints.csv",
        encoding="latin1"
    )

    df["created_at"] = pd.to_datetime(
        df["created_at"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["created_at"]
    )

    df = df.drop(
        columns=[
            "title",
            "description",
            "sub_category_id",
            "category_id",
            "civic_agency_id",
            "address",
        ],
        errors="ignore"
    )

    df = df.dropna(
        subset=[
            "ward_title",
            "category_title"
        ]
    )

    df["civic_agency_title"] = (
        df["civic_agency_title"]
        .fillna("Unknown")
    )

    df["category_title"] = (
        df["category_title"]
        .replace(CATEGORY_REMAP)
    )

    df["year"] = (
        df["created_at"]
        .dt.year
    )

    df["month"] = (
        df["created_at"]
        .dt.to_period("M")
    )

    df["latitude"] = pd.to_numeric(
        df.get("latitude"),
        errors="coerce"
    )

    df["longitude"] = pd.to_numeric(
        df.get("longitude"),
        errors="coerce"
    )

    df["is_resolved"] = (
        df["complaint_status_title"]
        == "Resolved"
    )

    df["is_open"] = (
        df["complaint_status_title"]
        == "Open"
    )

    return df


@st.cache_data
def prepare_map_data(df):

    map_data = df.copy()

    map_data["latitude"] = pd.to_numeric(
        map_data["latitude"],
        errors="coerce"
    )

    map_data["longitude"] = pd.to_numeric(
        map_data["longitude"],
        errors="coerce"
    )

    map_data = map_data.dropna(
        subset=[
            "latitude",
            "longitude"
        ]
    )

    map_data = map_data[
        (
            map_data["latitude"]
            .between(-90, 90)
        )
        &
        (
            map_data["longitude"]
            .between(-180, 180)
        )
    ]

    return map_data