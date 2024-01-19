# data importer
import pandas as pd
import yfinance as yf

import numpy as np
from matplotlib import pyplot as plt


atrLength = 10

# Ticker data import
ticker = '^GSPC'
yfticker= yf.Ticker(ticker)

mkt_data = yfticker.history(start="2020-01-01", interval="1D")
mkt_data = mkt_data.assign(symbol=ticker)

mkt_data['Range'] = mkt_data['High'] - mkt_data['Low']

mkt_data['TrueRange'] = pd.concat([mkt_data['High'], mkt_data['Close'].shift()], axis=1).max(axis=1) \
           - pd.concat([mkt_data['Low'], mkt_data['Close'].shift()], axis=1).min(axis=1)

mkt_data['ATR'] = mkt_data['TrueRange'].rolling(window=atrLength).mean()


print(mkt_data)

print(mkt_data['Range'].tail(15))



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

