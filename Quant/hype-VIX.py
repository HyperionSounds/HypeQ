# data importer
import pandas as pd
import yfinance as yf

import numpy as np
from matplotlib import pyplot as plt



# Ticker data import
vticker = '^VIX'
vfticker= yf.Ticker(vticker)

vol_data = vfticker.history(start="2004-01-01", interval="1D")
vol_data = vol_data.assign(symbol=vticker)
print(vol_data.tail)


fig = plt.figure(figsize=(15, 7))
ax3 = fig.add_subplot(1, 1, 1)
vol_data['Close'].plot(ax=ax3)
ax3.set_xlabel('Date')
ax3.set_ylabel('VIX')
ax3.set_title('Implied Volatility')
plt.show()


print(vol_data)


#Example for importing multiple tickers
#full_data = yf.download("SPY ^VIX", start="2004-01-01")
#print(full_data)