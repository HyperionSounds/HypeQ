#griswald nigga
import numpy as np
import pandas as pd
from datetime import timedelta
from datetime import datetime as dt
import time
import yfinance as yf
import matplotlib.pyplot as plt

atrLength = 10

if __name__ == "__main__":  

    START = '2018-01-30'
    END = '2024-01-17'

    tickers = ['ES=F'] 
    adj_close_list = []
    for ticker in tickers:
        ticker_module = yf.Ticker(ticker)
        data = yf.download(ticker, start=START, end=END)
        adj_close = data['Adj Close']
        adj_close.rename(f'{ticker} Adj Close', inplace=True)
        adj_close_list.append(adj_close)

    mkt_data = data
    mkt_data = mkt_data.reset_index()

    print('mkt_data: ', mkt_data)
    mkt_data['Range'] = mkt_data['High'] - mkt_data['Low']

    mkt_data['TrueRange'] = pd.concat([mkt_data['High'], mkt_data['Close'].shift()], axis=1).max(axis=1) \
           - pd.concat([mkt_data['Low'], mkt_data['Close'].shift()], axis=1).min(axis=1)

    mkt_data['ATR'] = mkt_data['TrueRange'].rolling(window=atrLength).mean()

    print(mkt_data)

    input_range = mkt_data['Range'].iloc[-1]
    print("range: ", input_range)

    # Calculate the absolute difference in range for each day compared to the last day
    mkt_data['RangeDifference'] = abs(mkt_data['Range'] - input_range)

    # calculatres and prints 10 days with most similar range
    mkt_data_range_days = mkt_data.iloc[(mkt_data['Range']-input_range).abs().argsort()[:10]]
    print(mkt_data_range_days)

    predicted_range_days = mkt_data.loc[mkt_data.index.intersection(mkt_data_range_days.index)]
    #predicted_range_days = data.loc[mkt_data_range_days.index + 1]

    #drops last day
    predicted_range_days = predicted_range_days[:-1]
    print(predicted_range_days)

    # if we are still using datetime index
    #next_day_index = mkt_data_range_days.index + timedelta(days=1)

    #last_selected_index = predicted_range_days.index
    #next_rows = mkt_data.loc[last_selected_index + 1:]
    #print('next rows: ', next_rows)


    next_day_index = [predicted_range_days.index + 1]
    # Extract the DataFrame for the next day
    next_day_data = mkt_data.loc[next_day_index]

    print("Next day after the 10 days with most similar range:")
    print(next_day_data)

    print('no way we made it here')