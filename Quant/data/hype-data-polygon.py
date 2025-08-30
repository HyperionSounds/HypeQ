import requests
import pandas as pd
import datetime as dt

POLYGON_API_KEY = "VPW919sxTSkgKfvBveVePscFxExszmHt"

def get_polygon_ohlcv(symbol, start="2020-05-31"):
    start_date = dt.datetime.strptime(start, "%Y-%m-%d").date()
    end_date = dt.date.today()

    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}"
    params = {
        "adjusted": "true",
        "sort": "asc",
        "limit": 50000,   # max per call
        "apiKey": POLYGON_API_KEY
    }

    r = requests.get(url, params=params)
    data = r.json()

    if "results" not in data:
        raise RuntimeError(f"Polygon error: {data}")

    df = pd.DataFrame(data["results"])
    df["t"] = pd.to_datetime(df["t"], unit="ms")
    df = df.rename(columns={
        "t": "Date",
        "o": "Open",
        "h": "High",
        "l": "Low",
        "c": "Close",
        "v": "Volume"
    })
    df = df.set_index("Date")
    return df[["Open", "High", "Low", "Close", "Volume"]]
    print(df)

# Example usage
if __name__ == "__main__":
    ticker_data = get_polygon_ohlcv("AAPL", start="2024-07-31")
    print(ticker_data)
    print(ticker_data.head())
