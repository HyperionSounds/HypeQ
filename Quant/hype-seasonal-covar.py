import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import datetime as dt

# Get the stock ticker
tickers ='ES=F'

# Set the start date, ending date is today
start=dt.datetime(1970,1,1)
end = dt.datetime.now()

# Download stock data
assets=yf.download(tickers,start,end) #['Adj Close']

# Renaming to humane column names
assets.rename(columns={'Adj Close': 'Adj_Close'}, inplace=True)

# Checking what the data looks like
assets.head()

# Compute daily returns using pandas pct_change()
assets['daily_returns'] = assets['Adj_Close'].pct_change()

# Skip first row with NA 
#assets = assets['daily_returns'][1:]
assets = assets[1:]

# Do a plot to check time series
plt.plot(assets['daily_returns'])


# Break time series into first and second half of the year

first_half = assets[assets.index.month.isin([1,2,3,4,11,12])]
second_half = assets[assets.index.month.isin([5,6,7,8,9,10])]

# Check first half data
first_half.head()

# Calculate the cumulative daily returns for first half of year
first_half['FH_Culm_Return'] = (1 + first_half['daily_returns']).cumprod() - 1

# Plot first half data transform for sanity check
plt.plot(first_half['FH_Culm_Return'])


# Calculate the cumulative daily returns for second half of year
second_half['SH_Culm_Return'] = (1 + second_half['daily_returns']).cumprod() - 1

# Plot first half data transform for sanity check
plt.plot(second_half['SH_Culm_Return'])

# Prepare series for concatentation
s1 = first_half['FH_Culm_Return']
s2 = second_half['SH_Culm_Return']

# Fill NaN with last value
s1.fillna(method='ffill', inplace=True)
s2.fillna(method='ffill', inplace=True)

# Concat series together and set to out df
out = pd.concat([s1, s2], axis=1)

# Fill NaN with last value
out.fillna(method ='ffill', inplace=True)
out

# This step is optional, you can resample to 1 month or leave as-is
#out = out.resample('1M').asfreq().ffill()

# Plot the final results of the two series. 
plt.figure(figsize=(20,5))
plt.title(tickers+" Seasonal Performance")
plt.xlabel('Year')
plt.ylabel('Culmulative Perf')
plt.plot(out.FH_Culm_Return, color = "black", label='Nov-Apr')
plt.plot(out.SH_Culm_Return, color = "red", label='May-Oct')
plt.legend()
plt.show()