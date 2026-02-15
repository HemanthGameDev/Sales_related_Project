import pandas as pd

def load_and_clean_data(file_path):
    """
    Reads the CSV, handles missing values, and creates new features.
    """
    df = pd.read_csv(file_path)
    
    # Handle Missing Prices using Category Mean
    df['Unit_Price'] = df['Unit_Price'].fillna(
        df.groupby('Category')['Unit_Price'].transform('mean')
    )
    
    # Feature Engineering
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    df['Total_Revenue'] = df['Quantity'] * df['Unit_Price']
    df['Month'] = df['Order_Date'].dt.strftime('%B')
    
    # Crucial: Sort months so they don't appear alphabetically (Jan, Feb, March...)
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)
    
    return df