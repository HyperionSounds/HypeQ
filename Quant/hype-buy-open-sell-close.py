import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

# Define the start and end dates
START = '2025-04-01'
END = '2025-08-27'

# Define the tickers
TICKERS = ['ES=F','NQ=F']

def backtest_buy_close_sell_open(ticker):
    data = yf.download(ticker, start=START, end=END)

    # Ensure data has both Open and Close
    if 'Open' not in data.columns or 'Close' not in data.columns:
        print(f"Missing data for {ticker}")
        return None

    # Drop missing values
    data = data[['Open', 'Close']].dropna()

    # Align close-to-open return (buy at close of day t, sell at open of day t+1)
    data['Close_Buy'] = data['Close'].shift(0)
    data['Open_Sell'] = data['Open'].shift(-1)

    # Strategy return = (next day open / previous close) - 1
    data['Return'] = data['Open_Sell'] / data['Close_Buy'] - 1

    # Drop final row since it has no next-day open
    data = data[:-1]

    # Cumulative return (assuming $1 initial capital)
    data['Cumulative_Return'] = (1 + data['Return']).cumprod()

    return data

# Run backtest and plot results
plt.figure(figsize=(12, 6))

for ticker in TICKERS:
    result = backtest_buy_close_sell_open(ticker)
    if result is not None:
        plt.plot(result.index, result['Cumulative_Return'], label=ticker)

plt.title('Buy Close / Sell Open Strategy (Cumulative Returns)')
plt.xlabel('Date')
plt.ylabel('Cumulative Return (Starting at $1)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()