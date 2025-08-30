import finnhub

#client = finnhub.Client(api_key="d2n8d4hr01qn3vmjuolgd2n8d4hr01qn3vmjuom0")
#quote = client.quote("AAPL")

#print(quote)



import requests
import pandas as pd
import datetime as dt

FINNHUB_API_KEY = "d2n8d4hr01qn3vmjuolgd2n8d4hr01qn3vmjuom0"

def get_finnhub_ohlcv(symbol, start="2020-05-31"):
    start_ts = int(dt.datetime.strptime(start, "%Y-%m-%d").timestamp())
    end_ts = int(dt.datetime.now().timestamp())

    url = "https://finnhub.io/api/v1/stock/candle"
    params = {
        "symbol": symbol,
        "resolution": "D",  # free tier only
        "from": start_ts,
        "to": end_ts,
        "token": FINNHUB_API_KEY
    }

    r = requests.get(url, params=params)
    data = r.json()

    if data.get("s") != "ok":
        raise RuntimeError(f"Finnhub error: {data}")

    df = pd.DataFrame({
        "Open": data["o"],
        "High": data["h"],
        "Low": data["l"],
        "Close": data["c"],
        "Volume": data["v"]
    }, index=pd.to_datetime(data["t"], unit="s"))

    df.index.name = "Date"
    return df

if __name__ == "__main__":
    df = get_finnhub_ohlcv("AAPL", start="2024-07-31")
    print(df.head())




    
