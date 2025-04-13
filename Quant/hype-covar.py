import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

start = '2020-01-01'
end = '2024-07-26'

tick1 = 'AAPL'
tick2 = 'SPY'

# Fetching the data
qqq = yf.Ticker(tick1)
qqq_price = qqq.history(start=start, end=end)['Close']
qqq_price.name = tick1

aapl = yf.Ticker(tick2)
aapl_price = aapl.history(start=start, end=end)['Close']
aapl_price.name = tick2

prices = pd.concat([qqq_price, aapl_price], axis=1)

def daily_returns(prices):
    res = (prices / prices.shift(1) - 1.0)[1:]
    return res

def cumulative_returns(returns):
    res = (returns + 1.0).cumprod()
    return res

cum_returns = cumulative_returns(daily_returns(prices))

# Calculating rolling covariance
rolling_cov = cum_returns[tick1].rolling(window=30).cov(cum_returns[tick2])

# Plotting the prices and rolling covariance
fig, ax1 = plt.subplots(figsize=(14, 7))

color = 'tab:blue'
ax1.set_xlabel('Date')
ax1.set_ylabel('Price', color=color)
ax1.plot(prices.index, prices[tick1], label=('Price', tick1), color='blue', alpha=0.6)
ax1.plot(prices.index, prices[tick2], label=('Price', tick2), color='orange', alpha=0.6)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Rolling Covariance', color=color)
ax2.plot(rolling_cov.index, rolling_cov, label='Rolling Covariance', color='red', alpha=0.6)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))

plt.title('QQQ and AAPL Prices with Rolling Covariance')
plt.show()

# Printing the covariance and beta values
cov = cum_returns.cov()
Beta = cov.iloc[0][1] / cov.iloc[0][0]
print(f"Covariance matrix:\n{cov}")
print(f"Beta: {Beta}")

# Linear regression to find beta and alpha
res = cum_returns.copy()
res['one'] = 1.0
beta, alpha = np.linalg.lstsq(res[[tick1, 'one']], res[tick2], rcond=None)[0]
print(f'Linear Regression Beta: {beta}, Alpha: {alpha}')