# 🏙️ City Complaint Intelligence System

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Open%20App-brightgreen)](https://city-complaint-intelligence-system.streamlit.app/)

## 🚀 Overview
This project analyzes real-world civic complaint data to identify patterns, hotspots, and inefficiencies in urban service systems.

It transforms raw complaint data into actionable insights that can help city authorities improve decision-making and service delivery.

---

## 🎯 Problem Statement
Urban local bodies receive thousands of complaints related to infrastructure, sanitation, and public services. However, these complaints are rarely analyzed to:

- Identify high-risk areas  
- Understand dominant issue categories  
- Measure resolution efficiency  
- Detect service gaps  

---

## 💡 Solution
This system provides an interactive dashboard that:

- Analyzes complaint trends over time  
- Identifies high-density problem areas  
- Evaluates resolution performance  
- Highlights inefficiencies in service delivery  

---

## 📊 Key Features

### 📈 Data Analysis
- Category-wise complaint distribution  
- Yearly and monthly trends  
- Status distribution (Open, Resolved, etc.)  

### 🗺️ Geospatial Insights
- Complaint location scatter visualization  
- Density heatmap to identify hotspots  

### 🧠 Intelligent Insights
- Automated insights based on real data  
- Identification of top problem areas  
- Main issue detection for selected ward  

### ⚙️ Performance Metrics
- Resolution efficiency (%) KPI  
- Agency-wise performance comparison  
- Ward-wise complaint vs resolution analysis  

### 🎛️ Interactive Dashboard
- Filters for Year, Ward, and Agency  
- Dynamic updates across all visuals  

### ⬇️ Export Feature
- Download filtered dataset for further analysis  

---

## 📌 Key Insights

- Infrastructure-related issues (roads, garbage, lighting) dominate complaints  
- Complaint volume dropped significantly during COVID period  
- Certain wards consistently report higher complaint density  
- A large percentage of complaints remain unresolved, indicating inefficiencies  

---

## 🛠️ Tech Stack

- **Python**  
- **Pandas** – Data processing  
- **Matplotlib & Seaborn** – Visualization  
- **Streamlit** – Interactive dashboard  
- **GitHub Codespaces** – Development environment  

---

## ▶️ How to Run Locally

```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

## 📅 Data Source
Public civic complaint dataset (2019–2022)
Contains ~16,000+ complaint records with location, category, and status
## 📈 Project Structure

```
City-Complaint-Intelligence-System/
│
├── dashboard.py
├── requirements.txt
├── Log of complaints.csv
└── README.md
```
## 📸 Dashboard Preview

This dashboard provides an overview of complaint trends, categories, and resolution performance.
<img width="1360" height="609" alt="image" src="https://github.com/user-attachments/assets/0ba24ec7-7f75-43c9-928c-2016493cacbd" />

## 🔥 Complaint Heatmap

<img width="1161" height="768" alt="image" src="https://github.com/user-attachments/assets/2798c3ab-9135-4bbe-80fc-a5f8f5f05165" />


## 📊 Why This Project Matters

This project demonstrates how data analytics can be used to:

- Improve public service delivery
- Identify infrastructure gaps
- Support data-driven governance
- Enhance citizen experience

## 🧠 Learnings

- Handling real-world messy data
- Feature engineering and data cleaning
- Building interactive dashboards
- Extracting actionable insights from raw data

## 📌 Future Improvements

- Add real-time data integration
- Implement complaint prediction (ML model)
- Improve map visualization with advanced libraries
- Build API-based backend for scalability

## 👨‍💻 Author

- Vara Prasad K -Aspiring Data Analyst
