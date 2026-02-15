import streamlit as st
import pandas as pd
import plotly.express as px
from src.data_loader import load_real_retail_data, perform_segmentation

st.set_page_config(page_title="Retail Analytics Pro", layout="wide")

st.title("📊 Real-Time Retail Insights Dashboard")
st.markdown("This dashboard analyzes **500,000+ real transactions** to identify growth trends.")

# --- DATA LOADING ---
with st.spinner('⏳ Processing 500,000+ transactions... This may take a minute.'):
    df = load_real_retail_data()
    # Adding the Machine Learning layer
    rfm_df = perform_segmentation(df)

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Options")
countries = sorted(df['Country'].unique())
# Defaulting to UK as it has the most data
selected_country = st.sidebar.selectbox("Select Country", countries, index=countries.index('United Kingdom'))

# Filter data
filtered_df = df[df['Country'] == selected_country]

# --- KPI SECTION ---
st.subheader(f"📍 Market Performance: {selected_country}")
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"£{filtered_df['TotalPrice'].sum():,.2f}")
col2.metric("Total Orders", f"{len(filtered_df):,}")
col3.metric("Avg. Order Value", f"£{filtered_df['TotalPrice'].mean():,.2f}")

# --- VISUALIZATION SECTION ---
col_left, col_right = st.columns(2)

with col_left:
    st.write("### 🔝 Top 10 Best Selling Products")
    top_products = filtered_df.groupby('Description')['TotalPrice'].sum().sort_values(ascending=False).head(10)
    # Streamlit's built-in bar chart
    st.bar_chart(top_products)

with col_right:
    st.write("### 🤖 AI Customer Segments (Global)")
    # Using Plotly for a professional, interactive Pie Chart
    segment_counts = rfm_df['Segment_Name'].value_counts().reset_index()
    segment_counts.columns = ['Segment', 'Count']
    
    fig = px.pie(segment_counts, values='Count', names='Segment', 
                 color_discrete_sequence=px.colors.sequential.RdBu,
                 hole=0.4) # Makes it a clean Donut Chart
    st.plotly_chart(fig, use_container_width=True)

# --- BUSINESS INSIGHT ---
st.info(f"💡 **Insight:** In {selected_country}, your top product alone generates £{top_products.iloc[0]:,.2f}. Focus marketing spend here.")