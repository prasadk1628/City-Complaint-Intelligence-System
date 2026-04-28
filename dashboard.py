# 1️⃣ Imports
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 2️⃣ App Title
st.set_page_config(page_title="City Complaint Intelligence", layout="wide")
st.title("City Complaint Intelligence System")

# 3️⃣ Load + Clean Data
@st.cache_data
def load_data():
    return pd.read_csv("Log of complaints.csv", encoding='latin1')

df = load_data()

df['created_at'] = pd.to_datetime(df['created_at'], format='mixed')

df = df.drop(columns=[
    'title', 'description', 'sub_category_id',
    'category_id', 'civic_agency_id', 'address'
])

df = df.dropna(subset=['ward_title', 'category_title'])
df['civic_agency_title'] = df['civic_agency_title'].fillna('Unknown')

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

df['year'] = df['created_at'].dt.year

st.markdown(f"📅 Data Last Updated: {df['created_at'].max().date()}")

# 4️⃣ Filters
st.sidebar.header("Filters")

year_options = ["All"] + sorted(df['year'].unique().tolist())
selected_year = st.sidebar.selectbox("Select Year", year_options)

selected_ward = st.sidebar.selectbox(
    "Select Ward",
    ["All"] + sorted(df['ward_title'].unique().tolist())
)
selected_agency = st.sidebar.selectbox(
    "Select Agency",
    ["All"] + sorted(df['civic_agency_title'].unique().tolist())
)

filtered_df = df.copy()

if selected_year != "All":
    filtered_df = filtered_df[filtered_df['year'] == selected_year]

if selected_ward != "All":
    filtered_df = filtered_df[filtered_df['ward_title'] == selected_ward]

if selected_agency != "All":
    filtered_df = filtered_df[filtered_df['civic_agency_title'] == selected_agency]

ward_df = filtered_df[filtered_df['ward_title'] != 'Other']

#Top Wards vs Resolution Rate
st.subheader("🏙️ Top Wards vs Resolution Rate")

ward_stats = (
    ward_df.groupby('ward_title')
    .agg(
        complaints=('ward_title', 'count'),
        resolution_rate=('complaint_status_title', lambda x: (x == 'Resolved').mean() * 100)
    )
    .sort_values('complaints', ascending=False)
    .head(10)
)

st.bar_chart(ward_stats)

# 5️⃣ KPI Section
st.subheader("📊 Key Insights")

col1, col2, col3 = st.columns(3)

col1.metric("Total Complaints", len(filtered_df))
col2.metric("Open Complaints (%)", round((filtered_df['complaint_status_title'] == 'Open').mean() * 100, 2))
col3.metric("Resolved Complaints (%)", round((filtered_df['complaint_status_title'] == 'Resolved').mean() * 100, 2))

resolved = (filtered_df['complaint_status_title'] == 'Resolved').sum()
total = len(filtered_df)
efficiency = (resolved / total) * 100 if total > 0 else 0


# 6️⃣ Insight Explanation
st.subheader("📌 Key Observations")

unresolved_pct = 100 - efficiency

st.write(f"""
• Infrastructure-related issues (roads, garbage, lighting) dominate complaint categories  
• Complaint volume shows a sharp drop during COVID period  
• Certain wards consistently report higher complaint density  
• Over {round(unresolved_pct, 2)}% complaints remain unresolved  
""")

# 7️⃣ Core Charts
st.subheader("Top Complaint Categories")
st.bar_chart(filtered_df['category_title'].value_counts().head(10))

st.subheader("Yearly Complaint Trend")
st.line_chart(filtered_df.groupby('year').size())

st.subheader("Complaint Status Distribution")
st.bar_chart(filtered_df['complaint_status_title'].value_counts())

#Agency Resolution Performance
st.subheader("🏢 Agency Resolution Performance (%)")

agency_perf = (
    filtered_df.groupby('civic_agency_title')['complaint_status_title']
    .apply(lambda x: (x == 'Resolved').mean() * 100)
    .sort_values(ascending=False)
)

st.dataframe(agency_perf.head(10).to_frame(name='Resolution Rate (%)'))

#Download Data
st.subheader("⬇️ Download Data")

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="filtered_complaints.csv",
    mime="text/csv"
)



# 8️⃣ Location Intelligence
st.subheader("🚨 Top Problem Areas")

top_wards = (
    ward_df.groupby('ward_title')
    .size()
    .sort_values(ascending=False)
    .head(5)
)

st.write(top_wards)

st.subheader("📍 Main Issue in Selected Area")

if selected_ward != "All":
    top_issue = (
        filtered_df['category_title']
        .value_counts()
        .head(1)
    )
    st.write(top_issue)
else:
    st.write("Select a ward to see its main issue")


# 9️⃣ Maps Section
st.subheader("Complaint Locations Map (Fallback View)")

map_data = filtered_df[['latitude', 'longitude']].dropna()
map_data['latitude'] = pd.to_numeric(map_data['latitude'], errors='coerce')
map_data['longitude'] = pd.to_numeric(map_data['longitude'], errors='coerce')
map_data = map_data.dropna()

fig, ax = plt.subplots()
ax.scatter(
    map_data['longitude'],
    map_data['latitude'],
    s=1,
    alpha=0.5
)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_title("Complaint Locations (Scatter Map)")
st.pyplot(fig)

st.subheader("Complaint Density Heatmap")

fig2, ax2 = plt.subplots()
sns.kdeplot(
    x=map_data['longitude'],
    y=map_data['latitude'],
    cmap="Reds",
    fill=True,
    bw_adjust=0.5,
    ax=ax2
)
ax2.set_title("Complaint Hotspots")
ax2.set_xlabel("Longitude")
ax2.set_ylabel("Latitude")
st.pyplot(fig2)

# 1️⃣0️⃣ Category vs Status Heatmap
st.subheader("🔥 Category vs Status Heatmap")

pivot = pd.crosstab(
    filtered_df['category_title'],
    filtered_df['complaint_status_title']
)

fig3, ax3 = plt.subplots()

sns.heatmap(pivot, cmap="Reds", annot=False, ax=ax3)

ax3.set_xlabel("Status")
ax3.set_ylabel("Category")

st.pyplot(fig3)


# 1️⃣0️⃣ System Performance
st.subheader("⚙️ Resolution Efficiency")
st.metric("Resolution Rate (%)", round(efficiency, 2))

# 1️⃣0️⃣ Automated Insight
st.subheader("🧠 Automated Insight")

if efficiency < 40:
    st.warning("Low resolution rate indicating  inefficiency in complaint handling.")
elif efficiency < 70:
    st.info("Moderate performance in resolving complaints.")
else:
    st.success("Good resolution performance observed.")

# 1️⃣1️⃣ Advanced Insight
st.subheader("📈 Peak Complaint Month")

monthly = filtered_df.groupby(filtered_df['created_at'].dt.to_period("M")).size()
peak_month = monthly.idxmax()
st.write(f"Highest complaints recorded in: {peak_month}")

# 1️⃣2️⃣ About Section
st.markdown("""
---
### About :
This project analyzes real-world civic complaint data to identify patterns,
hotspots, and inefficiencies in urban service systems using data analytics.
""")