# data importer
import pandas as pd
import yfinance as yf

import numpy as np
from matplotlib import pyplot as plt

# Ticker data import
ticker = 'SPY'
yfticker= yf.Ticker(ticker)

mkt_data = yfticker.history(start="2004-01-01", interval="1D")
mkt_data = mkt_data.assign(symbol=ticker)
print(mkt_data.tail)


#Historical Volatility calculation
TRADING_DAYS = 252
returns = np.log(mkt_data['Close']/mkt_data['Close'].shift(1))
returns.fillna(0, inplace=True)
volatility = returns.rolling(window=TRADING_DAYS).std()*np.sqrt(TRADING_DAYS)
sharpe_ratio = returns.mean()/volatility
sharpe_ratio.tail()



fig = plt.figure(figsize=(15, 7))
ax3 = fig.add_subplot(1, 1, 1)
sharpe_ratio.plot(ax=ax3)
ax3.set_xlabel('Date')
ax3.set_ylabel('Sharpe ratio')
ax3.set_title('Sharpe ratio with the annualized volatility')


#mkt_data.plot(ax=ax)



plt.show()






