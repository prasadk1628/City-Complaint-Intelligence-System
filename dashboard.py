import streamlit as st
import pandas as pd

st.set_page_config(page_title="City Complaint Intelligence", layout="wide")

st.title("City Complaint Intelligence System")

# Load data
df = pd.read_csv("Log of complaints.csv", encoding='latin1')

# --- Cleaning ---
df['created_at'] = pd.to_datetime(df['created_at'], format='mixed')

df = df.drop(columns=[
    'title', 'description', 'sub_category_id',
    'category_id', 'civic_agency_id', 'address'
])

df = df.dropna(subset=['ward_title', 'category_title'])
df['civic_agency_title'] = df['civic_agency_title'].fillna('Unknown')

# Category normalization
df['category_title'] = df['category_title'].replace({
    'Streetlights': 'Street lighting',
    'Roads and Footpaths': 'Mobility - Roads, Footpaths and Infrastructure',
    'Mobility - Roads, Public transport': 'Mobility - Roads, Footpaths and Infrastructure',
    'Water Supply': 'Water Supply and Services',
    'Electricity & Power': 'Electricity and Power Supply',
    'Power supply': 'Electricity and Power Supply',
    'Solid Waste Management': 'Garbage and Unsanitary Practices',
    'Waste Management': 'Garbage and Unsanitary Practices'
})

# ✅ Create year column ONCE
df['year'] = df['created_at'].dt.year

# --- Filters ---
st.sidebar.header("Filters")

year_options = ["All"] + sorted(df['year'].unique().tolist())
selected_year = st.sidebar.selectbox("Select Year", year_options)

selected_ward = st.sidebar.selectbox(
    "Select Ward",
    ["All"] + sorted(df['ward_title'].unique().tolist())
)

# ✅ Correct filtering logic
filtered_df = df.copy()

if selected_year != "All":
    filtered_df = filtered_df[filtered_df['year'] == selected_year]

if selected_ward != "All":
    filtered_df = filtered_df[filtered_df['ward_title'] == selected_ward]

# --- Metrics ---
st.subheader("📊 Key Insights")

col1, col2, col3 = st.columns(3)

col1.metric("Total Complaints", len(filtered_df))
col2.metric("Open Complaints (%)", round((filtered_df['complaint_status_title'] == 'Open').mean()*100, 2))
col3.metric("Resolved Complaints (%)", round((filtered_df['complaint_status_title'] == 'Resolved').mean()*100, 2))

# --- Top Categories ---
st.subheader("Top Complaint Categories")
st.bar_chart(filtered_df['category_title'].value_counts().head(10))

# --- Yearly Trend ---
st.subheader("Yearly Complaint Trend")
st.line_chart(filtered_df.groupby('year').size())

# --- Status Distribution ---
st.subheader("Complaint Status Distribution")
st.bar_chart(filtered_df['complaint_status_title'].value_counts())



import matplotlib.pyplot as plt

st.subheader("Complaint Locations Map (Fallback View)")

map_data = filtered_df[['latitude', 'longitude']].dropna()

map_data['latitude'] = pd.to_numeric(map_data['latitude'], errors='coerce')
map_data['longitude'] = pd.to_numeric(map_data['longitude'], errors='coerce')

map_data = map_data.dropna()

# Plot using matplotlib
fig, ax = plt.subplots()

ax.scatter(
    map_data['longitude'],
    map_data['latitude'],
    s=1,   # small dots
    alpha=0.5
)

ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_title("Complaint Locations (Scatter Map)")

st.pyplot(fig)