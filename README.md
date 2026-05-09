# 🏙️ CivicLens — Urban Complaint Analytics

> *Municipal complaint data, when properly analyzed, contains clear and actionable signals for urban governance.*

An end-to-end analytics project on 16,000+ civic complaints — identifying service gaps, resolution failures, and high-risk urban zones to support data-driven decision-making.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Open%20App-brightgreen)](https://city-complaint-intelligence-system.streamlit.app/)
[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://city-complaint-intelligence-system.streamlit.app/)

---

## 📌 Problem Statement

Urban local bodies in India receive thousands of complaints monthly — roads, garbage, drainage, lighting — yet most of this data goes unanalyzed. Without systematic analysis, city authorities cannot:

- Identify which wards are consistently underserved
- Measure how efficiently agencies resolve complaints
- Detect seasonal or category-specific spikes before they escalate
- Allocate maintenance budgets based on actual demand

This project applies exploratory data analysis to a real municipal complaint log to answer those questions directly.

---

## 📊 Dataset

| Property | Detail |
|---|---|
| File | `complaints_log.csv` |
| Records | ~16,000+ complaint entries |
| Period | 2019 – 2022 |
| Source | Public civic complaint dataset (municipal corporation log) |

<details>
<summary><b>📋 Column Reference (click to expand)</b></summary>

| Original Column | Renamed To | Description |
|---|---|---|
| `Complaint_ID` | `complaint_id` | Unique identifier |
| `Date_Logged` | `date_logged` | Date complaint was filed |
| `Ward_No` | `ward_number` | Administrative ward |
| `Category` | `complaint_category` | Issue type (Roads, Garbage, Drainage, etc.) |
| `Sub_Category` | `complaint_subcategory` | Specific issue description |
| `Status` | `resolution_status` | Open / In Progress / Resolved / Closed |
| `Agency` | `responsible_agency` | Department assigned to resolve |
| `Latitude` | `latitude` | GPS latitude |
| `Longitude` | `longitude` | GPS longitude |
| `Resolution_Date` | `date_resolved` | Date resolved (if applicable) |

> All columns renamed to snake_case for clarity. `HSC` fields in raw data refer to Hyderabad Sub-Category codes — replaced with human-readable values.

</details>

---

## 🧹 Data Cleaning

| Step | Action |
|---|---|
| Column naming | Standardized all headers to snake_case |
| Date parsing | Converted mixed string formats to `datetime` |
| Duplicates | Dropped 214 fully duplicate rows |
| `date_resolved` nulls | Retained (expected for open complaints) — added `is_resolved` boolean flag |
| `latitude/longitude` nulls | ~4% missing — excluded from map viz only, retained elsewhere |
| `responsible_agency` nulls | ~1.2% missing — labeled `"Unassigned"` |
| Date outliers | Removed 11 records with `date_logged` before 2015 (data entry errors) |

**Engineered features:**
- `resolution_days` = `date_resolved - date_logged`
- `complaint_year`, `complaint_month` extracted from `date_logged`
- `is_resolved` boolean flag

---

## 🔍 Key Findings

### 📈 Volume Trends
- Complaints peaked in **2019–2020**, then dropped sharply in mid-2020 due to COVID-19 lockdowns
- Volume recovered in 2021 but did not return to pre-pandemic levels by end of 2022
- **Highest-complaint months:** October–November consistently (post-monsoon infrastructure damage)

### 🗂️ Category Distribution
- Top 3 categories: **Roads & Footpaths (~34%), Garbage & Sanitation (~27%), Drainage (~18%)**
- These three alone account for **~79% of all complaints**
- Electrical/Lighting complaints are low in volume but show the worst resolution rates

### ⚙️ Resolution Performance
| Metric | Value |
|---|---|
| Overall resolution rate | ~61% |
| Average resolution time | 18.4 days |
| Worst-performing agency | Drainage & Sewerage Board (median 34 days) |
| Best-performing agency | Solid Waste Management (89% resolution rate) |

### 🗺️ Ward-Level Analysis
- Top 5 complaint-heavy wards account for **~23% of all complaints**
- High-complaint wards are concentrated in older infrastructure zones
- Several wards show both high complaint volume *and* low resolution rates — a double failure signal

---

## 💡 Business Insights

**1. Three complaint types consume 79% of resources — fix them to fix the system.**
Roads, garbage, and drainage dominate. Targeted investment in these three areas addresses the majority of citizen grievances. Generic budget distribution across all categories is inefficient.

**2. A 61% resolution rate is a governance problem, not a data problem.**
Nearly 4 in 10 complaints remain open or stale. The dashboard surfaces exactly *which agencies* are failing and *which wards* they're failing in — directly actionable.

**3. Post-monsoon (Oct–Nov) is the highest-risk window.**
Complaint spikes follow the monsoon season consistently. Preventive maintenance scheduled for August–September could reduce reactive complaint volume by an estimated 15–20%.

**4. Five wards need prioritized attention.**
These wards show both high volume and low resolution — the highest citizen dissatisfaction risk. Any ward-level resource reallocation should start here.

**5. The 2020 volume drop is a data artifact, not a service improvement.**
Normalization is needed before any year-on-year comparison for reporting purposes.

---

## ✅ Conclusion

The three most immediate decisions this analysis supports:

- **Redirect maintenance budgets** toward the top 3 complaint categories
- **Set SLA targets per agency** based on current median resolution times
- **Pre-position resources** in high-risk wards before the monsoon season

The live Streamlit dashboard allows planners to filter by year, ward, and agency — making this not just a retrospective report but a usable decision-support tool.

---

## 📸 Screenshots

### Dashboard Overview
![Dashboard](image-3.png)

### Complaint Heatmap by Ward
![Heatmap](image-4.png)

### Category vs Status Heatmap
![Category vs Status](image-5.png)

### Dataset & Code
<p>
  <img src="image-2.png" width="48%"/>
  <img src="image.png" width="48%"/>
</p>

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.10 | Core analysis language |
| Pandas | Data cleaning & transformation |
| Matplotlib / Seaborn | Static visualizations |
| Streamlit | Interactive web dashboard |
| GitHub Codespaces | Development environment |

---

## ▶️ Run Locally

```bash
git clone https://github.com/prasadk1628/City-Complaint-Intelligence-System.git
cd City-Complaint-Intelligence-System
pip install -r requirements.txt
streamlit run dashboard.py
```

---

## 📁 Project Structure

```
City-Complaint-Intelligence-System/
│
├── dashboard.py                 # Streamlit app
├── requirements.txt             # Dependencies
├── complaints_log.csv           # Cleaned dataset
├── Log of complaints.ipynb      # Full EDA notebook
└── README.md
```

---

## 🔮 Future Improvements

- Complaint volume **forecasting** using ARIMA / Prophet for peak period prediction
- **Real-time data** integration via civic API
- **Ward comparison** view — side-by-side resolution performance
- Lightweight **complaint classification model** using NLP on sub-category text

---

## 📄 License

Licensed under the [MIT License](LICENSE).

---

## 👤 Author

**Vara Prasad K** — Aspiring Data Analyst | Python · SQL · Streamlit

[![Email](https://img.shields.io/badge/Email-kavalivaraprasad16@gmail.com-D14836?logo=gmail&logoColor=white)](mailto:kavalivaraprasad16@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-vara--prasad--k-0077B5?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vara-prasad-k-4a6026230/)
[![GitHub](https://img.shields.io/badge/GitHub-prasadk1628-181717?logo=github&logoColor=white)](https://github.com/prasadk1628)
