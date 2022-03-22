import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

import io, base64, os, json, re
import pandas as pd
import numpy as np
import datetime

#much of this script is based on code provided here: https://www.viralml.com/static/code/ViralML-Hands-on-Inverted-Yield-Curve.html
#must download treasury data from the feds website via xml scraper UST, and import CSV to working directory, or from one of the garbage sources commented out below

"""
# load data you donwloaded from Yahoo Finance
#gspc_df = pd.read_csv('^GSPC.csv') #SP500
#gspc_df['Date'] = pd.to_datetime(gspc_df['Date'])


# gotta go download data here: https://data.nasdaq.com/data/USTREASURY/YIELD-treasury-yield-curve-rates
# the data is kind of shitty
rates_df = pd.read_csv('USTREASURY-YIELD.csv')
rates_df['Date'] = pd.to_datetime(rates_df['Date'])
print(rates_df.head())
"""

# download rates.csv from ust folder package.
rates_df = pd.read_csv('rates.csv')
rates_df.columns = ['date', '1M', '3M', '6M', '1Y', '2Y', '3Y', '5Y', '7Y', '10Y', '20Y', '30Y', '30Y Display']

recent_rates = rates_df.tail

rates = recent_rates
print(rates)

fig = plt.figure(figsize=(16, 8))
plt.plot(rates_df['date'],rates_df['10Y'])
plt.plot(rates_df['date'],rates_df['5Y'])
plt.plot(rates_df['date'],rates_df['2Y'])
plt.suptitle('rates_df')

# Now going to compare long vs short rates and the delta (risk)
# join both datasets together
fig, ax = plt.subplots(figsize=(16, 8))

plt.plot(rates_df['date'], rates_df['10Y'] - rates_df['2Y'] , color='r', label='Long minus Short Rates')

plt.legend()
plt.grid()
plt.axhline(0)
plt.show()


#if you have adjusted close data (i.e. zipline)
"""
# Get second axis
ax2 = ax.twinx()
plt.plot(together['date'],
         together['Adj Close']
         , 'c', label='S&P 500')
plt.legend()
plt.title('Rates VS S&P 500')
ax2.tick_params('vals', colors='b')

# join both datasets together (if you were to have timeseries of stock / mkt index data)
together = pd.merge(gspc_df[['date', 'Adj Close']],
                    rates_df[['date', '3Y', '5Y']],
                    on= ['Date'], how='left')


# get percent change for all interested values
together['3YR_PCT'] = together['3 YR'].pct_change()
together['5YR_PCT'] = together['5 YR'].pct_change()
together['SP500_PCT'] = together['Adj Close'].pct_change()
together.head()

tmp = together.copy()
cut_off_date = '1990-01-01'
tmp = tmp[tmp['date'] > cut_off_date]

tmp['diff'] = tmp['5 YR'] - tmp['3 YR']

# join both datasets together
fig, ax = plt.subplots(figsize=(16, 8))

plt.plot(tmp['date'], tmp['diff'].rolling(window=5).mean().values,
         color='r',
         linewidth=1, label='       Rates PCT')
plt.legend()
plt.grid()
plt.axhline(0)
ax.tick_params('vals', colors='r')

# background bar color
tmp['diff_simple'] = tmp['diff'].rolling(window=5).mean().values
tmp['diff_simple']  = [-100 if val > 0 else 100 for val in tmp['diff_simple'].values]
ax.pcolorfast(ax.get_xlim(), ax.get_ylim(),
              tmp['diff_simple'].values[np.newaxis],
              cmap='Paired', alpha=0.3)

# Get second axis
ax2 = ax.twinx()
plt.plot(tmp['date'],
         tmp['Adj Close'].rolling(window=5).mean().values
         , 'c--', label='S&P 500 PCT')
plt.legend()
plt.title('Rates Diff VS S&P 500')
ax2.tick_params('vals', colors='b')
"""


#formatter 
"""
#formatter in the works
fig, ax = plt.subplots()
ax.plot(rates_df['date'],rates_df['10Y'])

myFmt = DateFormatter("%y")
ax.xaxis.set_major_formatter(myFmt)

plt.grid()
plt.show()
"""
