
import pandas as pd
import json
import os
from tvDatafeed import TvDatafeed, Interval

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(os.path.join(parent_dir, "company_training_data"), exist_ok=True)
tv = TvDatafeed(username="username", password="password")
# Fetch historical data for each company
symbol = "ABAN.N0000"
cse_data = tv.get_hist(
    symbol="ABAN.N0000",
    exchange="CSELK",
    interval=Interval.in_daily,
    n_bars=600
)
print(cse_data)
# Save to CSV
#cse_data.to_csv(os.path.join(parent_dir, f'company_training_data/{symbol.replace(" ", "_")}.csv'), index=False)
