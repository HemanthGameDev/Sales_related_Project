import streamlit as st
import pandas as pd
import plotly.express as px
from src.data_loader import load_real_retail_data, perform_segmentation

st.set_page_config(page_title="Retail Intel Pro", layout="wide")

st.title("📊 Advanced Retail Intelligence Platform")

# --- DATA LOADING ---
with st.spinner('⏳ Initializing Data Engine...'):
    df = load_real_retail_data()
    if df.empty:
        st.error("Data could not be loaded. Please check your source or local files.")
        st.stop()

# --- SIDEBAR: DYNAMIC CONTROLS ---
st.sidebar.header("🔍 Intelligent Search & Filters")

# 1. Market Selection
countries = sorted(df['Country'].unique())
selected_country = st.sidebar.selectbox("Select Market", countries, index=countries.index('United Kingdom'))
country_df = df[df['Country'] == selected_country]

# 2. Date Range Filter
min_date = country_df['InvoiceDate'].min().date()
max_date = country_df['InvoiceDate'].max().date()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

# 3. Product Search Box (Text-based search)
search_term = st.sidebar.text_input("Search Product Name (e.g., 'WHITE', 'HEART')")

# 4. Specific Product Multiselect
all_products = sorted(country_df['Description'].unique().tolist())
selected_products = st.sidebar.multiselect("Filter by Specific Products", all_products)

# 5. Metric Selector
metric_choice = st.sidebar.radio("Analyze Performance By:", ["TotalPrice", "Quantity"])
metric_label = "Total Revenue (£)" if metric_choice == "TotalPrice" else "Units Sold"

# --- DATA PROCESSING ---
# Apply Date Filter
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = country_df[(country_df['InvoiceDate'].dt.date >= start_date) & 
                             (country_df['InvoiceDate'].dt.date <= end_date)]
else:
    filtered_df = country_df

# Apply Text Search Filter
if search_term:
    filtered_df = filtered_df[filtered_df['Description'].str.contains(search_term, case=False, na=False)]

# Apply Specific Product Multiselect Filter
if selected_products:
    filtered_df = filtered_df[filtered_df['Description'].isin(selected_products)]

# --- MAIN DASHBOARD ---
# KPI Cards
col1, col2, col3 = st.columns(3)
col1.metric("Selected Revenue", f"£{filtered_df['TotalPrice'].sum():,.2f}")
col2.metric("Orders Found", f"{len(filtered_df):,}")
col3.metric("Avg. Price", f"£{filtered_df['UnitPrice'].mean():,.2f}")

# --- DYNAMIC PLOTTING ---
st.write(f"### 📈 Performance Analysis: {metric_label}")

if not filtered_df.empty:
    # Time Series Graph: Revenue/Quantity over time
    daily_trend = filtered_df.groupby(filtered_df['InvoiceDate'].dt.date)[metric_choice].sum().reset_index()
    fig_line = px.area(daily_trend, x='InvoiceDate', y=metric_choice, 
                       title=f"Daily {metric_label} Trend",
                       labels={metric_choice: metric_label, 'InvoiceDate': 'Date'})
    st.plotly_chart(fig_line, use_container_width=True)

    col_left, col_right = st.columns(2)
    
    with col_left:
        st.write("### 📦 Top Product Comparison")
        top_prod = filtered_df.groupby('Description')[metric_choice].sum().sort_values(ascending=False).head(10).reset_index()
        fig_bar = px.bar(top_prod, x=metric_choice, y='Description', orientation='h',
                         title=f"Top 10 Products by {metric_label}",
                         color=metric_choice, color_continuous_scale='Viridis')
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_right:
        st.write("### 🤖 AI Market Segments")
        # Run AI Analysis with the safety check from data_loader
        rfm_df = perform_segmentation(filtered_df)
        
        if "Insufficient Data" in rfm_df['Segment_Name'].values:
            st.warning("⚠️ Not enough unique customers in this selection for AI Clustering. Try broadening your filters.")
        else:
            segment_counts = rfm_df['Segment_Name'].value_counts().reset_index()
            segment_counts.columns = ['Segment', 'Count']
            fig_pie = px.pie(segment_counts, values='Count', names='Segment', 
                             hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig_pie, use_container_width=True)
else:
    st.warning("No data found for the selected filters. Please broaden your search criteria!")

st.info("💡 **Pro-Tip:** Use the search box to find patterns for specific product keywords across different dates.")