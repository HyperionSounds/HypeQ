# pulls minute futures data from yahoo. API only allows for a 7 day period pulled, sometime in the last 30 days.

import pandas as pd
from pandas_datareader.data import DataReader
import pandas_datareader as dr
import datetime as dt

import pytz

import yfinance as yf

ticker = 'SPY'
yfticker= yf.Ticker(ticker)

ticker_data = yfticker.history(start="2020-05-31", interval="1D")
ticker_data = ticker_data.assign(symbol=ticker)
#ticker_data['symbol'] = ticker_data['symbol'].str.replace(r'', '')

ticker_data.index.names = ['date']
ticker_data.index = ticker_data.index.map(lambda t: t.strftime('%Y-%m-%d %H:%M'))

#adds a column for date
#ticker_data['date'] = ticker_data.index

#makes a nice format for zipline ingest ohlcv format
ticker_data.rename(columns={
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Volume': 'volume',
    }, inplace=True, copy=False)

ticker_data = ticker_data[['symbol','open','high','low','close','volume']]

#pd.set_option('display.max_rows', None)
print(ticker_data)