import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE SETUP ---
st.set_page_config(
    page_title="E-commerce Sales Dashboard",
    page_icon="📈",
    layout="wide"
)

# --- DATA LOADING AND PREPARATION ---
# Load the dataset from the CSV file.
df = pd.read_csv("ecommerce_dataset_10000.csv")

# Convert numeric Excel dates to datetime objects.
df['order_date'] = pd.to_datetime(df['order_date'], unit='D', origin='1899-12-30')

# Create a 'sales' column by multiplying quantity and unit_price.
df['sales'] = df['quantity'] * df['unit_price']

# Create a 'month_year' column for the line chart.
df['month_year'] = df['order_date'].dt.to_period('M').astype(str)

# --- MAIN DASHBOARD ---
st.title("📈 E-commerce Sales Dashboard")
st.markdown("---")

# --- KEY METRICS ---
total_sales = int(df['sales'].sum())
total_orders = df['order_id'].nunique()
total_customers = df['customer_id'].nunique()
total_products = df['product_id'].nunique()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Sales", value=f"${total_sales:,}")
with col2:
    st.metric(label="Total Orders", value=f"{total_orders:,}")
with col3:
    st.metric(label="Total Customers", value=f"{total_customers:,}")
with col4:
    st.metric(label="Total Products", value=f"{total_products:,}")

st.markdown("---")

# --- VISUALIZATIONS ---
left_column, right_column = st.columns(2)

# Chart 1: Sales by Country (Map)
with left_column:
    st.subheader("Sales by Country")
    sales_by_country = df.groupby('country')['sales'].sum().reset_index()
    fig_map = px.choropleth(
        sales_by_country,
        locations='country',
        locationmode='country names',
        color='sales',
        hover_name='country',
        color_continuous_scale=px.colors.sequential.Plasma,
        title='Global Sales Distribution'
    )
    fig_map.update_layout(title_x=0.5)
    st.plotly_chart(fig_map, use_container_width=True)

# Chart 2: Sales by Category (Bar Chart)
with right_column:
    st.subheader("Sales by Category")
    sales_by_category = df.groupby('category')['sales'].sum().reset_index().sort_values(by='sales', ascending=False)
    fig_bar = px.bar(
        sales_by_category,
        x='category',
        y='sales',
        text_auto='.2s',
        title='Top Performing Categories'
    )
    fig_bar.update_layout(title_x=0.5)
    st.plotly_chart(fig_bar, use_container_width=True)

# Chart 3: Sales by Month (Line Chart)
with left_column:
    st.subheader("Sales by Month")
    sales_by_month = df.groupby('month_year')['sales'].sum().reset_index()
    fig_line = px.line(
        sales_by_month,
        x='month_year',
        y='sales',
        markers=True,
        title='Monthly Sales Trend'
    )
    fig_line.update_layout(title_x=0.5)
    st.plotly_chart(fig_line, use_container_width=True)

# Chart 4: Sales by Payment Method (Pie Chart)
with right_column:
    st.subheader("Sales by Payment Method")
    sales_by_payment = df.groupby('payment_method')['sales'].sum().reset_index()
    fig_pie = px.pie(
        sales_by_payment,
        names='payment_method',
        values='sales',
        title='Payment Method Distribution'
    )
    fig_pie.update_layout(title_x=0.5)
    st.plotly_chart(fig_pie, use_container_width=True)

    
