import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf  

# Define the start and end dates
START = '2014-01-01'
END = '2025-05-22'

# Define the tickers
tickers = ['SPY'] 

# Download the close prices for the tickers
close_list = []
for ticker in tickers:
    data = yf.download(ticker, start=START, end=END, group_by='column')  # Ensure flat columns
    print(data)
    if not data.empty:
        close = data['Close']
        close_list.append(close)
    else:
        print(f"No data returned for {ticker}")

# Check if we have valid data
if len(close_list) == 0:
    raise ValueError("No valid data downloaded. Exiting.")

# Use the close prices for SPY
SPY = close_list[0]

# Calculate daily returns
r = SPY.pct_change()

# Calculate monthly returns
Monthly_Returns = r.groupby([r.index.year.rename('year'), r.index.month.rename('month')]).mean()
Monthly_Returns = Monthly_Returns.dropna()  # Drop NaNs before plotting

# Create a DataFrame for monthly returns
Monthly_Returns_List = Monthly_Returns.reset_index()
Monthly_Returns_List.columns = ['Year', 'Month', 'Monthly_Return']

# Plot settings
from pylab import rcParams
rcParams['figure.figsize'] = 20, 10

# Plot the boxplot
Monthly_Returns_List.boxplot(column='Monthly_Return', by='Month')
ax = plt.gca()
labels = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
ax.set_xticklabels(labels)
plt.tick_params(axis='both', which='major', labelsize=15)
plt.title('Monthly Returns Boxplot')
plt.suptitle('')
plt.xlabel('Month')
plt.ylabel('Monthly Return')
plt.show()