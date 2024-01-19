# data importer
import pandas as pd
import yfinance as yf

import numpy as np
from matplotlib import pyplot as plt

#Example for importing multiple tickers
#full_data = yf.download("SPY ^VIX", start="2004-01-01")
#print(full_data)

# Ticker data import
ticker = '^GSPC'
yfticker= yf.Ticker(ticker)

mkt_data = yfticker.history(start="2020-01-01", interval="1D")
mkt_data = mkt_data.assign(symbol=ticker)


#Historical Volatility calculation
TRADING_DAYS = 30
returns = np.log(mkt_data['Close']/mkt_data['Close'].shift(1))
returns.fillna(0, inplace=True)
volatility = returns.rolling(window=TRADING_DAYS).std()*np.sqrt(TRADING_DAYS)
volatility.tail()

#VIX stuff and volatility
vticker = '^VIX'
vfticker= yf.Ticker(vticker)
imp_vol = vfticker.history(start="2004-01-01", interval="1D")
imp_vol = imp_vol.assign(symbol=vticker)
mkt_data['Returns']=returns
mkt_data['Volatility']=volatility
mkt_data['ImpliedVol']=imp_vol['Close']


mkt_data['VRP'] = mkt_data['ImpliedVol'].rank(pct = True) - mkt_data['Volatility'].rank(pct = True)

print(mkt_data['VRP'].tail(15))

#mkt_data.plot.scatter(x="Volatility", y="ImpliedVol", alpha=0.5)
print(mkt_data)

covariance = np.cov(mkt_data['ImpliedVol'],mkt_data['Close'], bias=True)[0][1]
print(covariance)


# Plotting stuff
plt.figure(figsize=(12,5))
plt.xlabel('Volatility')

ax1 = mkt_data.Close.plot(color='blue', grid=True, label='SPX')
ax2 = mkt_data.VRP.plot(color='red', grid=True, secondary_y=True, label='VRP')

h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()

plt.legend(h1+h2, l1+l2, loc=2)







# Just the VIX or whatever
fig = plt.figure(figsize=(15, 7))
ax4 = fig.add_subplot(1, 1, 1)
imp_vol['Close'].plot(ax=ax4)
ax4.set_xlabel('Date')
ax4.set_ylabel('VIX')
ax4.set_title('Implied Volatility')

#plotting two columns w similar scale
#mkt_data.plot(y=["Close", "ImpliedVol"])


plt.show()