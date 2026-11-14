import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Amazon Marketplace Analytics",
    page_icon="📊",
    layout="wide"
)

# 2. Database Connection Cached for Performance
@st.cache_resource
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Bunty764020",  # Replace with your MySQL root password
        database="amazon_marketplace_analytics"
    )

# 3. Load Data from MySQL View
@st.cache_data
def load_data():
    conn = get_db_connection()
    query = "SELECT * FROM vw_marketplace_executive_summary LIMIT 50000;" # Sample for fast rendering
    df = pd.read_sql(query, conn)
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Database connection failed: {e}")
    st.stop()

# 4. Sidebar Filters
st.sidebar.header("Filter Marketplace Data")
selected_shipping = st.sidebar.multiselect(
    "Select Shipping Method",
    options=df["shipping_method"].unique(),
    default=df["shipping_method"].unique()
)

# Apply Filter
filtered_df = df[df["shipping_method"].isin(selected_shipping)]

# 5. Dashboard Header
st.title("📦 Amazon Marketplace Executive Dashboard")
st.markdown("Real-time operational analytics and KPI tracking powered by your MySQL Star Schema Data Warehouse.")
st.markdown("---")

# 6. Top-Level KPI Metric Cards
total_orders = len(filtered_df)
total_revenue = filtered_df["payment_amount"].sum()
avg_delivery_days = filtered_df["delivery_days"].mean()
return_rate = (filtered_df["is_returned"].sum() / total_orders) * 100 if total_orders > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Orders", f"{total_orders:,}")
col2.metric("Total Revenue", f"${total_revenue:,.2f}")
col3.metric("Avg Delivery Days", f"{avg_delivery_days:.1f} days")
col4.metric("Return Rate", f"{return_rate:.2f}%")

st.markdown("---")

# 7. Charts Section
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("Revenue by Payment Method")
    pay_df = filtered_df.groupby("payment_method")["payment_amount"].sum().reset_index()
    fig_pay = px.pie(pay_df, names="payment_method", values="payment_amount", hole=0.4, color_discrete_sequence=px.colors.sequential.Teal)
    st.plotly_chart(fig_pay, use_container_width=True)

with row1_col2:
    st.subheader("Delivery Status Breakdown")
    status_df = filtered_df.groupby(["shipping_method", "delivery_status"]).size().reset_index(name="count")
    fig_status = px.bar(status_df, x="shipping_method", y="count", color="delivery_status", barmode="group", color_discrete_sequence=px.colors.qualitative.Bold)
    st.plotly_chart(fig_status, use_container_width=True)

# 8. Raw Data Preview
with st.expander("🔍 View Raw Relational Data Preview"):
    st.dataframe(filtered_df.head(100))