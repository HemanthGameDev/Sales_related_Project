import matplotlib.pyplot as plt

def generate_dashboard(df):
    """
    Takes a cleaned DataFrame and generates a 2-plot dashboard.
    """
    # 1. Prepare Data for Plotting
    # We group by month and product name (Assuming these columns exist after cleaning)
    monthly_trend = df.groupby('Month')['Total_Revenue'].sum()
    top_products = df.groupby('Product')['Quantity'].sum().sort_values(ascending=False)

    # 2. Create the Figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Plot 1: Monthly Trends (Line Chart)
    monthly_trend.plot(kind='line', marker='o', ax=ax1, color='green', linewidth=2)
    ax1.set_title('📈 Revenue Trend by Month', fontsize=14)
    ax1.set_ylabel('Revenue (INR)')
    ax1.grid(True, linestyle='--', alpha=0.6)
    
    # Plot 2: Product Popularity (Bar Chart)
    top_products.plot(kind='bar', ax=ax2, color='orange', edgecolor='black')
    ax2.set_title('📦 Units Sold per Product', fontsize=14)
    ax2.set_ylabel('Quantity Sold')

    plt.tight_layout()
    plt.show()
    
    print("✅ Dashboard generated successfully!")