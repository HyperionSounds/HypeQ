from lppls import lppls
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
import matplotlib.pyplot as plt

# 60 days of data
END = datetime.now()
START = END - timedelta(days=40)

# Ticker list
TICKERS = ['ES=F']

def analyze_ticker(ticker):
    print(f"Downloading 15m data for {ticker}...")
    data = yf.download(
        ticker,
        start=START,
        end=END,
        interval="15m",
        progress=False,
        prepost=True,  # Optional: includes pre/post-market data for stocks
    )

    if data.empty:
        print(f"No data for {ticker}.")
        return

    print(data)
    # Reset index and ensure datetime column is used
    data = data.reset_index()
    data = data[['Datetime', 'Close']].dropna()

    # Make sure 15-min candles are visible in the chart
    time = np.array([
        t.toordinal() + t.hour / 24 + t.minute / 1440
        for t in data['Datetime']
    ])
    price = np.log(data['Close'].values).flatten()
    observations = np.array([time, price])

    # Fit LPPLS
    model = lppls.LPPLS(observations=observations)
    try:
        tc, m, w, a, b, c, c1, c2, O, D = model.fit(max_searches=25)
    except Exception as e:
        print(f"Fit failed: {e}")
        return

    # Plot LPPLS fit
    model.plot_fit()
    plt.title(f'{ticker} LPPLS Fit (15m)')
    plt.xlabel('Date')
    plt.ylabel('ln(p)')
    plt.show()

    # Confidence indicator
    try:
        res = model.mp_compute_nested_fits(
            workers=4,
            window_size=480,  # 480 * 15m = ~5 days of trading
            smallest_window_size=120,
            outer_increment=4,
            inner_increment=8,
            max_searches=25
        )
        model.plot_confidence_indicators(res)
        plt.title(f'{ticker} Bubble Confidence (15m)')
        plt.show()
    except Exception as e:
        print(f"Confidence indicator failed: {e}")

def main():
    print("Running LPPLS (15-min candles)...")
    for ticker in TICKERS:
        analyze_ticker(ticker)
    print("Done.")

if __name__ == "__main__":
    main()