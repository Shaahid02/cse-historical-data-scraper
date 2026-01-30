import requests
import pandas as pd
import time
from datetime import datetime

def get_tradingview_history(symbol, exchange="CSELK", interval="1D", start="2021-01-01", end=None):
    start_ts = int(time.mktime(datetime.strptime(start, "%Y-%m-%d").timetuple()))
    end_ts = int(time.time()) if end is None else int(time.mktime(datetime.strptime(end, "%Y-%m-%d").timetuple()))

    full_symbol = f"{exchange}:{symbol}"

    url = "https://tvc4.tradingview.com/history"

    params = {
        "symbol": full_symbol,
        "resolution": interval,
        "from": start_ts,
        "to": end_ts
    }

    resp = requests.get(url, params=params, headers={"User-Agent": "Mozilla/5.0"})

    try:
        data = resp.json()
    except Exception as e:
        raise Exception(f"Failed to decode response for {symbol}. Raw response:\n{resp.text}") from e

    if "t" not in data:
        raise Exception(f"No data for {symbol}. Response: {data}")

    df = pd.DataFrame({
        "date": [datetime.fromtimestamp(x) for x in data["t"]],
        "open": data["o"],
        "high": data["h"],
        "low": data["l"],
        "close": data["c"],
        "volume": data["v"],
    })

    return df


# Example usage
df = get_tradingview_history("ABAN.N0000", start="2021-01-01")
print(df.head(), df.tail())
