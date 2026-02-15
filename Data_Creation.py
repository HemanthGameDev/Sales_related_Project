import pandas as pd
import numpy as np

# Creating a messy dataset with 500 rows
data = {
    'Order_Date': pd.date_range(start='2025-01-01', periods=500, freq='D'),
    'Product': np.random.choice(['Laptop', 'Mouse', 'Monitor', 'Keyboard', 'Headphones'], 500),
    'Category': np.random.choice(['Electronics', 'Accessories'], 500),
    'Quantity': np.random.randint(1, 10, 500),
    'Unit_Price': np.random.uniform(500, 50000, 500),
    'Customer_ID': np.random.randint(1000, 1100, 500)
}

df_raw = pd.DataFrame(data)
# Intentionally adding some "Dirty" data (NaNs)
df_raw.loc[::50, 'Unit_Price'] = np.nan 

df_raw.to_csv('retail_data.csv', index=False)
print("✅ Proper dataset 'retail_data.csv' created!")