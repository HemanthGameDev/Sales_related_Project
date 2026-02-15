from src.data_loader import load_and_clean_data
from src.visualizer import generate_dashboard

# 1. Define the path to your data
DATA_PATH = 'retail_data.csv'

def start_analysis():
    print("🚀 Starting Retail Analytics Tool...")
    
    # 2. Load and Clean
    cleaned_df = load_and_clean_data(DATA_PATH)
    
    # 3. Generate Visuals
    generate_dashboard(cleaned_df)

if __name__ == "__main__":
    start_analysis()