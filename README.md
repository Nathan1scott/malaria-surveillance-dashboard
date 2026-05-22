# 🦟 Malaria Surveillance Dashboard - WHO AFRO

[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://python.org)
[![Dash](https://img.shields.io/badge/Dash-4.1.0-red)](https://dash.plotly.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![WHO Data](https://img.shields.io/badge/Data-WHO%20AFRO-brightgreen)](https://data.afro.who.int)

> An AI-powered malaria surveillance and outbreak prediction dashboard for Sub-Saharan Africa using real WHO AFRO data.

---

## 📋 Problem Statement

Malaria kills **over 600,000 people annually** in Sub-Saharan Africa – mostly children under 5. Health ministries lack real-time, data-driven tools to track outbreaks and allocate resources effectively.

**The Gap:** Without predictive analytics, malaria outbreaks catch communities unprepared, leading to preventable deaths.

**The Solution:** An interactive dashboard that visualizes historical WHO AFRO malaria data, identifies high-burden countries, and predicts outbreak risk using weather patterns.

---

## 🎯 Key Features

| Feature | Description |
|---------|-------------|
| **Real WHO AFRO Data** | Official malaria surveillance data for 10+ African countries |
| **Country & Year Filters** | Dynamic filtering to explore specific regions and time periods |
| **KPI Cards** | Total cases, deaths, positivity rate at a glance |
| **Trend Analysis** | Year-over-year case trends with interactive charts |
| **Seasonal Heatmap** | Visualize malaria patterns by month and country |
| **Outbreak Prediction** | ML-powered risk scoring using weather data (temp, rainfall, humidity) |
| **Export Insights** | Download filtered data as CSV for further analysis |
| **Mobile Responsive** | Works on phones, tablets, and desktops |

---

## 📊 Data Source

**Organization:** WHO AFRO Health Data Hub  
**License:** Creative Commons Attribution 4.0 (CC-BY-4.0)  
**Countries:** Nigeria, DR Congo, Uganda, Mozambique, Ghana, Kenya, Mali, Niger, Burkina Faso, Ivory Coast  
**Time Period:** 2018-2024  
**Data Points:** Confirmed malaria cases, deaths, test positivity rates

> *Data is publicly available and free to use for research and public health purposes.*

---

## 🛠️ Technology Stack

| Category | Technologies |
|----------|--------------|
| **Frontend** | Dash, Plotly, HTML/CSS |
| **Backend** | Python, Flask |
| **Data Processing** | Pandas, NumPy |
| **Machine Learning** | Scikit-learn, Random Forest |
| **Visualization** | Plotly Express, Matplotlib |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/Nathan1scott/malaria-surveillance-dashboard.git
cd malaria-surveillance-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
python malaria_dashboard.py
