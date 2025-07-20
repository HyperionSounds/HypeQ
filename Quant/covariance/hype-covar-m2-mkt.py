import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from pandas_datareader.data import DataReader

# === Parameters ===
start = '2018-01-01'
end = '2024-07-26'
fred_series = 'M2SL'  # M2 Money Supply, seasonally adjusted
market_ticker = 'SPY'

# === Fetch M2 Data from FRED ===
m2_data = DataReader(fred_series, 'fred', start, end)
m2_data = m2_data.ffill()  # Fill any missing values
m2_data.columns = ['M2']

# Resample weekly/monthly FRED data to business daily using forward-fill
m2_data = m2_data.resample('B').ffill()

# === Fetch SPY Data from Yahoo ===
spy = yf.Ticker(market_ticker)
spy_data = spy.history(start=start, end=end)
spy_data = spy_data[['Close']].rename(columns={'Close': market_ticker})

# === Align Dates ===
# === Align Dates (fix tz-aware vs naive) ===
m2_data.index = m2_data.index.tz_localize(None)
spy_data.index = spy_data.index.tz_localize(None)

combined = pd.concat([m2_data, spy_data], axis=1).dropna()

# === Compute Daily Returns and Cumulative Returns ===
def daily_returns(prices):
    return prices.pct_change().dropna()

def cumulative_returns(returns):
    return (returns + 1).cumprod()

returns = daily_returns(combined)
cum_returns = cumulative_returns(returns)

# === Rolling Covariance ===
rolling_cov = cum_returns['M2'].rolling(window=30).cov(cum_returns[market_ticker])

# === Plotting ===
fig, ax1 = plt.subplots(figsize=(14, 7))

normalized = combined / combined.iloc[0]

color = 'tab:blue'
ax1.set_xlabel('Date')
ax1.set_ylabel('Price/Cum Return', color=color)
ax1.plot(normalized.index, normalized['M2'], label='Normalized M2', color='blue', alpha=0.6)
ax1.plot(normalized.index, normalized[market_ticker], label='Normalized SPY', color='orange', alpha=0.6)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Rolling Covariance (30D)', color=color)
ax2.plot(rolling_cov.index, rolling_cov, label='Rolling Covariance', color='red', alpha=0.6)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
plt.title('M2 Money Supply vs SPY with 30-Day Rolling Covariance')
plt.show()

# === Covariance Matrix and Beta Calculation ===
cov = cum_returns.cov()
Beta = cov.loc['M2', market_ticker] / cov.loc['M2', 'M2']
print(f"\nCovariance matrix:\n{cov}")
print(f"\nBeta: {Beta}")

# === Linear Regression ===
res = cum_returns.copy()
res['one'] = 1.0
beta, alpha = np.linalg.lstsq(res[['M2', 'one']], res[market_ticker], rcond=None)[0]
print(f'Linear Regression Beta: {beta}, Alpha: {alpha}')
