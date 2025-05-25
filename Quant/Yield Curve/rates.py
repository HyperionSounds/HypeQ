import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

import io, base64, os, json, re
import pandas as pd
import numpy as np
import datetime

import yfinance as yf

#much of this script is based on code provided here: https://www.viralml.com/static/code/ViralML-Hands-on-Inverted-Yield-Curve.html
#must download treasury data from the feds website via xml scraper UST, and import CSV to working directory, or from one of the garbage sources commented out below

"""
# load data you donwloaded from Yahoo Finance
#gspc_df = pd.read_csv('^GSPC.csv') #SP500
#gspc_df['Date'] = pd.to_datetime(gspc_df['Date'])
"""

# download rates.csv from ust folder package.
rates_df = pd.read_csv('rates.csv')
rates_df.columns = ['Date', '1M', '3M', '6M', '1Y', '2Y', '3Y', '5Y', '7Y', '10Y', '20Y', '30Y', '30Y Display']
#rates_df['Date'] = pd.to_datetime(rates_df['Date'])

rates_df = rates_df.set_index('Date', inplace=False)

print(rates_df)
rates_df.info()



#if you have adjusted close data 

# Get the data for the SPY (an ETF on the S&P 500 index) and the stock Apple by specifying the stock ticker, start Date, and end Date
#mkt_data = yf.download(['SPY', 'AAPL'],'2020-01-01','2022-03-18')
"""
mkt_data = yf.download('SPY','2020-01-01','2022-03-18')

# Plot the adjusted close prices
mkt_data["Close"].plot()
plt.show()

print(mkt_data.tail)

mkt_data.rename(columns={
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Volume': 'volume',
    }, inplace=True, copy=False)

mkt_data.index.names = ['Date']
mkt_data.index = mkt_data.index.map(lambda t: t.strftime('%Y-%m-%d'))
"""

ticker = 'SPY'
yfticker= yf.Ticker(ticker)

mkt_data = yfticker.history(start="2020-01-01", interval="1D")
mkt_data = mkt_data.assign(symbol=ticker)

close_data = mkt_data[['Close']]
close_data.reset_index(drop=True)

print(close_data)
close_data.info()


# merge bond yield rates with market data
together = rates_df.join(mkt_data)
print(together)

together['Date'] = together.index
together.info

rates_df['Date'] = together.index

# Now plot stuff

# Plots interest rates of 10Y, 5Y, 2Y bonds on same graph (shows curve flattening)
fig = plt.figure(figsize=(16, 8))
plt.plot(rates_df['Date'],rates_df['10Y'])
plt.plot(rates_df['Date'],rates_df['5Y'])
plt.plot(rates_df['Date'],rates_df['2Y'])
plt.suptitle('Interest Rates 10Y / 5Y / 2Y')
plt.grid()



# Now going to compare long vs short rates and the delta (risk)
# join both datasets together
fig, ax = plt.subplots(figsize=(16, 8))

plt.plot(rates_df['Date'], rates_df['10Y'] - rates_df['2Y'] , color='r', label='Long minus Short Rates (10Y-2Y)')

plt.legend()
plt.grid()
plt.axhline(0)

# Get second axis
ax2 = ax.twinx()
plt.plot(together['Date'],
         together['Close']
         , 'c', label='S&P 500')
plt.legend()
plt.title('Rates VS S&P 500')
ax2.tick_params('both', colors='b')
plt.grid()


# last valid observation forward
together = together.fillna(method='ffill')

# drop NAs
together = together.dropna(axis=0)

together.tail(20)



# calculate delta between long and short rates
# get percent change for all interested values
together['3YR_PCT'] = together['3Y'].pct_change()
together['5YR_PCT'] = together['5Y'].pct_change()
together['SP500_PCT'] = together['Close'].pct_change()
together.head()

tmp = together.copy()
cut_off_date = '2020-01-01'
tmp = tmp[tmp['Date'] > cut_off_date]

tmp['diff'] = tmp['5Y'] - tmp['3Y']


# plotting mkt close and rates delta together
# join both datasets together
fig, ax = plt.subplots(figsize=(16, 8))

plt.plot(tmp['Date'], tmp['diff'].rolling(window=5).mean().values,
         color='r',
         linewidth=1, label='       Rates PCT')
plt.legend()
plt.grid()
plt.axhline(0)
ax.tick_params('both', colors='r')

# background bar color
tmp['diff_simple'] = tmp['diff'].rolling(window=5).mean().values
tmp['diff_simple']  = [-100 if val > 0 else 100 for val in tmp['diff_simple'].values]
ax.pcolorfast(ax.get_xlim(), ax.get_ylim(),
              tmp['diff_simple'].values[np.newaxis],
              cmap='Paired', alpha=0.3)

# Get second axis
ax2 = ax.twinx()
plt.plot(tmp['Date'],
         tmp['Close'].rolling(window=5).mean().values
         , 'c--', label='S&P 500 PCT')
plt.legend()
plt.title('Rates Diff VS S&P 500')
ax2.tick_params('both', colors='b')
plt.grid()
plt.show()