import pandas as pd
from sklearn.cluster import KMeans
import streamlit as st
import os

@st.cache_data
def load_real_retail_data():
    """
    Fetches data and shifts dates to the current year (2025-2026).
    """
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
    local_path = "retail_data.csv"
    
    try:
        df = pd.read_excel(url)
        df.to_csv(local_path, index=False)
    except Exception:
        if os.path.exists(local_path):
            df = pd.read_csv(local_path)
        else:
            return pd.DataFrame()

    # Standard Cleaning
    date_col = 'InvoiceDate' if 'InvoiceDate' in df.columns else 'Order_Date'
    id_col = 'CustomerID' if 'CustomerID' in df.columns else 'Customer_ID'
    
    df = df.dropna(subset=[id_col])
    df = df[df['Quantity'] > 0]
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    df[date_col] = pd.to_datetime(df[date_col])

    # --- THE DATE SHIFTER (The Fix!) ---
    # 1. Find the gap between the latest old date and today
    latest_old_date = df[date_col].max()
    current_date = pd.Timestamp.now()
    date_offset = current_date - latest_old_date
    
    # 2. Shift all dates forward so the data ends TODAY
    df[date_col] = df[date_col] + date_offset
    # -----------------------------------
    
    return df
def perform_segmentation(df):
    """
    Groups customers into segments using K-Means Clustering with validation.
    """
    # Dynamic column detection to prevent KeyErrors
    date_col = 'InvoiceDate' if 'InvoiceDate' in df.columns else 'Order_Date'
    id_col = 'CustomerID' if 'CustomerID' in df.columns else 'Customer_ID'
    inv_col = 'InvoiceNo' if 'InvoiceNo' in df.columns else 'Invoice_No'

    # 1. RFM Aggregation
    rfm = df.groupby(id_col).agg({
        date_col: lambda x: (df[date_col].max() - x.max()).days,
        inv_col: 'count',
        'TotalPrice': 'sum'
    })
    
    rfm.columns = ['Recency', 'Frequency', 'Monetary']
    
    # --- SAFETY CHECK: The "Bulletproof" Layer ---
    # We must have at least as many samples as clusters (3) to avoid ValueError
    if len(rfm) < 3:
        # Assign a default label if data is too small for AI
        rfm['Segment_Name'] = 'Insufficient Data for AI'
        return rfm
    
    # 2. K-Means Clustering
    kmeans = KMeans(n_clusters=3, init='k-means++', random_state=42)
    rfm['Segment'] = kmeans.fit_predict(rfm)
    
    # Mapping for the Dashboard
    segment_map = {0: 'At-Risk', 1: 'Potential', 2: 'Champions'}
    rfm['Segment_Name'] = rfm['Segment'].map(segment_map)
    
    return rfm