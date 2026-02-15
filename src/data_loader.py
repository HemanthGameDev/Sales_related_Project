import pandas as pd
from sklearn.cluster import KMeans
import streamlit as st
import os

@st.cache_data
def load_real_retail_data():
    """
    Fetches data from URL with a local fallback if internet fails.
    """
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
    local_path = "retail_data.csv"
    
    try:
        # Try fetching live data first
        df = pd.read_excel(url)
        df.to_csv(local_path, index=False) # Save backup
    except Exception:
        # Fallback to local file if internet is down
        if os.path.exists(local_path):
            df = pd.read_csv(local_path)
        else:
            return pd.DataFrame()

    # UCI Data uses 'InvoiceDate' and 'CustomerID'
    date_col = 'InvoiceDate' if 'InvoiceDate' in df.columns else 'Order_Date'
    id_col = 'CustomerID' if 'CustomerID' in df.columns else 'Customer_ID'
    
    df = df.dropna(subset=[id_col])
    df = df[df['Quantity'] > 0]
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    df[date_col] = pd.to_datetime(df[date_col])
    
    return df

def perform_segmentation(df):
    """
    Groups customers into segments using K-Means Clustering.
    """
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
    
    # 2. K-Means Clustering
    kmeans = KMeans(n_clusters=3, init='k-means++', random_state=42)
    rfm['Segment'] = kmeans.fit_predict(rfm)
    
    segment_map = {0: 'At-Risk', 1: 'Potential', 2: 'Champions'}
    rfm['Segment_Name'] = rfm['Segment'].map(segment_map)
    
    return rfm