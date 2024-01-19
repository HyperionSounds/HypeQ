# data importer
import pandas as pd
import yfinance as yf



ticker = '^GSPC'
yfticker= yf.Ticker(ticker)

mkt_data = yfticker.history(start="2004-01-01", interval="1D")
mkt_data = mkt_data.assign(symbol=ticker)
mkt_data.reset_index(level=0, inplace=True)


#full_data = yf.download("SPY ^VIX", start="2004-01-01")
#print(full_data)


#mkt_data.index = mkt_data.index.map(lambda t: t.strftime('%Y-%m-%d'))

#mkt_data['Date'] = mkt_data.index

#organized_data = mkt_data['Date','Open','High','Low','Close','Volume']


print(mkt_data.tail)
#print(mkt_data.Date)

#mkt_data = dt.strptime(str(mkt_data.Date), '%Y-%m-%d %H:%M') 


#close_data = mkt_data[['Close']]
#close_data.reset_index(drop=True)

#print(close_data)
#close_data.info()


print("Data imported")

mkt_data.to_csv('ticker_data.csv', index=False)  

print("Data exported")