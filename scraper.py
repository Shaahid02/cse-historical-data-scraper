import pandas as pd
import json
import os
from tvDatafeed import TvDatafeed, Interval
import time


project_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(project_dir, "company_training_data")
os.makedirs(output_dir, exist_ok=True)

company_data = []

try:
    with open(os.path.join(project_dir, 'company_data/data.json'), 'r', encoding='utf-8') as f:
        company_data = json.load(f)
except FileNotFoundError:
    company_data = []

print(f"Loaded {len(company_data)} companies from data.json")

# Initialize TvDatafeed once
tv = TvDatafeed(username="username", password="password")  # Replace with actual credentials


for company in company_data:
    symbol = company["symbol"]
    print(f"Processing symbol: {symbol}")
    try:
        cse_data = tv.get_hist(
            symbol=symbol,
            exchange="CSELK",
            interval=Interval.in_daily,
            n_bars=365
        )
        print(f"Fetched data for {symbol}: {len(cse_data) if cse_data is not None else 0} rows")
        if cse_data is not None and not cse_data.empty:
            print("First 5 rows:")
            print(cse_data.head())
            csv_path = os.path.join(output_dir, f'{symbol.replace(" ", "_")}.csv')
            print(f"Saving to: {csv_path}")
            cse_data.to_csv(csv_path, index=True)
        else:
            print(f"No data found for {symbol}")
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
    time.sleep(2)  # Add a delay to avoid rate limiting
