import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf  

# Define the start and end dates
START = '2014-01-01'
END = '2024-11-28'

# Define the tickers
tickers = ['SPY'] 

# Download the adjusted close prices for the tickers
adj_close_list = []
for ticker in tickers:
    data = yf.download(ticker, start=START, end=END)
    adj_close = data['Adj Close']
    adj_close.rename(f'{ticker} Adj Close', inplace=True)
    adj_close_list.append(adj_close)

# Use the adjusted close prices for SPY
SPY = adj_close_list[0]

# Calculate daily returns
r = SPY.pct_change()

# Calculate monthly returns
Monthly_Returns = r.groupby([r.index.year.rename('year'), r.index.month.rename('month')]).mean()

# Plot settings
from pylab import rcParams
rcParams['figure.figsize'] = 20, 10

# Create a DataFrame for monthly returns
Monthly_Returns_List = []
for i in range(len(Monthly_Returns)):
    Monthly_Returns_List.append({
        'Year': Monthly_Returns.index[i][0],
        'Month': Monthly_Returns.index[i][1],
        'Monthly_Return': Monthly_Returns.iloc[i]
    })
Monthly_Returns_List = pd.DataFrame(Monthly_Returns_List, columns=('Year', 'Month', 'Monthly_Return'))

# Plot the boxplot
Monthly_Returns_List.boxplot(column='Monthly_Return', by='Month')
ax = plt.gca()
labels = [item.get_text() for item in ax.get_xticklabels()]
labels = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

ax.set_xticklabels(labels)
plt.tick_params(axis='both', which='major', labelsize=15)
plt.title('Monthly Returns Boxplot')
plt.suptitle('')
plt.xlabel('Month')
plt.ylabel('Monthly Return')
plt.show()