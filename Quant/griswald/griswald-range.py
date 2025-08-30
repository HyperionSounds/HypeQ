import numpy as np
import pandas as pd
from datetime import timedelta
import datetime as dt
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns

# Settings
atrLength = 10
TRADING_DAYS = 30
tickers = ['ES=F']
START = '2018-01-30'
END = dt.datetime.now()

# === USER PARAMETERS ===
n = 5  # Number of recent days to compare
RangeDays = 30  # Number of similar historical patterns to look for
forward_days = 5  # How many days ahead to analyze
mkt_open = 6486  # Starting point for prediction

def get_forward_returns(df, reference_indices, n_days):
    results = []
    for idx in reference_indices:
        try:
            start_idx = df.index.get_loc(idx) + 1
            end_idx = start_idx + n_days
            if end_idx < len(df):
                forward_return = df['Close'].iloc[end_idx] - df['Open'].iloc[start_idx]
                results.append(forward_return)
        except:
            continue
    return results

# === Load Data ===
ticker = tickers[0]
data = yf.download(ticker, start=START, end=END)
mkt_data = data.copy()

# === Calculate Indicators ===
mkt_data['Range'] = mkt_data['High'] - mkt_data['Low']
mkt_data['Return'] = mkt_data['Close'] - mkt_data['Open']
mkt_data['TrueRange'] = pd.concat([mkt_data['High'], mkt_data['Close'].shift()], axis=1).max(axis=1) - \
                        pd.concat([mkt_data['Low'], mkt_data['Close'].shift()], axis=1).min(axis=1)
mkt_data['ATR'] = mkt_data['TrueRange'].rolling(window=atrLength).mean()

returns = np.log(mkt_data['Close'] / mkt_data['Close'].shift(1))
returns.fillna(0, inplace=True)
volatility = returns.rolling(window=TRADING_DAYS).std() * np.sqrt(TRADING_DAYS)

mkt_data['Returns'] = returns
mkt_data['Volatility'] = volatility

# === Build multi-day pattern vector ===
patterns = []
indices = []

for i in range(len(mkt_data) - n - forward_days):
    patterns.append(mkt_data['Return'].iloc[i:i+n].values)
    indices.append(mkt_data.index[i+n-1])

pattern_df = pd.DataFrame(patterns, index=indices)

# === Get current n-day pattern to match ===
latest_pattern = mkt_data['Return'].iloc[-n:].values

# === Find most similar historical patterns ===
pattern_df['Distance'] = pattern_df.apply(lambda row: np.linalg.norm(row[:n] - latest_pattern), axis=1)
similar_days = pattern_df.nsmallest(RangeDays, 'Distance')
similar_indices = similar_days.index

# === Collect forward returns after similar patterns ===
forward_returns = get_forward_returns(mkt_data, similar_indices, forward_days)
predicted_range = np.array(forward_returns) + mkt_open

# === Plot ===
plt.figure(figsize=(10, 6))
sns.histplot(predicted_range, bins=30, kde=True, color='skyblue', edgecolor='blue')
plt.title(f'Forward {forward_days}-Day Return After Similar {n}-Day Patterns')
plt.xlabel('Predicted Price')
plt.ylabel('Frequency')
plt.axvline(mkt_open, color='red', linestyle='--', label='Current Market')
plt.legend()
plt.tight_layout()
plt.show()
