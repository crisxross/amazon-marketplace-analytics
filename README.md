# 📦 Amazon Marketplace Executive Analytics & BI Dashboard

A full-stack, production-ready data pipeline and interactive business intelligence (BI) dashboard built to analyze 500,000+ transaction-mapped marketplace records. This project models a comprehensive e-commerce star schema, processes relational data through automated Python scripts, and serves real-time executive insights via Streamlit Cloud.

---

## 🚀 Live Demo & Architecture
* **Live App**: [View Deployed Streamlit Dashboard](#) *(Insert your Streamlit Cloud link here)*
* **Architecture**: Local MySQL Data Warehouse ➔ Python/Pandas Pipeline ➔ Static Cloud CSV Optimization ➔ Streamlit Community Cloud

---

## 🛠️ Tech Stack
* **Language**: Python 3.12
* **Data Processing & Manipulation**: Pandas, NumPy
* **Database & ORM**: MySQL, SQLAlchemy, MySQL Connector Python
* **Data Visualization**: Streamlit, Plotly Express
* **Version Control**: Git & GitHub

---

## 📊 Data Architecture & Star Schema
The underlying data warehouse follows a robust **Star Schema** design optimized for analytical queries:
* **Fact Tables**: `fact_orders`, `fact_shipments`, `fact_payments`, `fact_returns`
* **Dimension Tables**: `dim_customer`, `dim_product`, `dim_seller`, `dim_warehouse`, `dim_date`, `dim_geography`
* **Analytics Views**: `vw_marketplace_executive_summary` (Pre-aggregated executive metrics view)

---

## ✨ Key Dashboard Features
1. **Executive KPI Cards**: Real-time tracking of Total Orders, Total Revenue, Average Delivery Days, and Return Rates.
2. **Interactive Filtering**: Dynamic multi-select sidebar filtering by shipping methods and payment types.
3. **Advanced Visualizations**: 
   * Revenue breakdown by payment method (Donut chart).
   * Delivery status distributions grouped by logistics channels (Grouped bar chart).
4. **Data Transparency**: Expandable data preview drawer letting users inspect raw underlying relational records.

---

## 📂 Project Structure
```text
amazon-marketplace-analytics/
├── .gitignore
├── requirements.txt
└── src/
    ├── app.py                 # Main Streamlit dashboard application
    ├── db_connection.py       # SQLAlchemy database connection configuration
    ├── export_data.py         # ETL script to extract and export data warehouse views
    ├── marketplace_data.csv   # Production dataset optimized for cloud deployment
    └── generate_*.py          # Mock data generator scripts for pipeline simulation
