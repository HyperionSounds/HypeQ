import numpy as np
import pandas as pd
from datetime import timedelta
import datetime as dt
import time
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns

atrLength = 10

#number of days to look for to compare to
RangeDays = 10

#where you want to use as center for density function
mkt_open = 5522

def get_next_trading_days(mkt_data, selected_rows):
    # Create a function to find the next trading day (excluding weekends)
    def next_trading_day_index(current_index):
        next_index = current_index + pd.DateOffset(days=1)
        while next_index.weekday() >= 5:  # Skip weekends (Saturday and Sunday)
            next_index += pd.DateOffset(days=1)
        return next_index

    # Initialize an empty DataFrame to store the next trading day data
    next_days_data = pd.DataFrame()

    # Iterate through each index in selected_rows and get the next trading day
    for idx in selected_rows.index:
        next_trading_day = next_trading_day_index(idx)

        # Check if the next trading day is available in mkt_data
        if next_trading_day in mkt_data.index:
            next_day_data = mkt_data.loc[next_trading_day]
            next_days_data = pd.concat([next_days_data, next_day_data.to_frame().T])

    return next_days_data


if __name__ == "__main__":  

    START = '2018-01-30'
    #END = '2024-02-15'
    END = dt.datetime.now()

    tickers = ['ES=F'] 
    adj_close_list = []
    for ticker in tickers:
        ticker_module = yf.Ticker(ticker)
        data = yf.download(ticker, start=START, end=END)
        adj_close = data['Adj Close']
        adj_close.rename(f'{ticker} Adj Close', inplace=True)
        adj_close_list.append(adj_close)

    mkt_data = data
    print('mkt_data: ', mkt_data)

    # Calculates Range, TrueRange, and ATR and appends columns to mkt_data dataframe
    mkt_data['Range'] = mkt_data['High'] - mkt_data['Low']
    mkt_data['Return'] = mkt_data['Close']-mkt_data['Open']
    mkt_data['TrueRange'] = pd.concat([mkt_data['High'], mkt_data['Close'].shift()], axis=1).max(axis=1) \
           - pd.concat([mkt_data['Low'], mkt_data['Close'].shift()], axis=1).min(axis=1)
    mkt_data['ATR'] = mkt_data['TrueRange'].rolling(window=atrLength).mean()

    #Historical Volatility calculation
    TRADING_DAYS = 30
    returns = np.log(mkt_data['Close']/mkt_data['Close'].shift(1))
    returns.fillna(0, inplace=True)
    volatility = returns.rolling(window=TRADING_DAYS).std()*np.sqrt(TRADING_DAYS)
    volatility.tail()

    mkt_data['Returns']=returns
    mkt_data['Volatility']=volatility

    #print updated data
    print(mkt_data)

    # Finds similar days to last day
    #finds the input range from last trading day to use to find similar range days
    input_range = mkt_data['Return'].iloc[-1]
    print("range: ", input_range)

    # Calculate the absolute difference in range for each day compared to the last day, adds column to mkt_data frame 
    mkt_data['RangeDifference'] = abs(mkt_data['Return'] - input_range)

    # calculatres and prints 10 days with most similar range
    mkt_data_range_days = mkt_data.iloc[(mkt_data['Return']-input_range).abs().argsort()[:RangeDays]]
    print('most similar days: ', mkt_data_range_days)

    #selects same rows from our full dataset that exist in the sorted range days
    similar_range_days = mkt_data.loc[mkt_data.index.intersection(mkt_data_range_days.index)]
    #predicted_range_days = data.loc[mkt_data_range_days.index + 1]

    #drops last day
    similar_range_days = similar_range_days[:-1]
    print('similar range days: ', similar_range_days)

    # Use the function to get the next trading days for each day in similar_range_days
    next_trading_days_data = get_next_trading_days(mkt_data, similar_range_days)
    print("Next day after days with most similar range:")
    print('Next trading days data:')
    print(next_trading_days_data)

    #predict future range
    predicted_range = next_trading_days_data['Return'] + mkt_open
    print('predicted range: ', predicted_range)

    # histogram and density plot with seaborn
    sns.histplot(predicted_range.values, bins=30, kde=True, color='skyblue', edgecolor='blue')

    # Plot histogram
    plt.figure(figsize=(10, 6))
    plt.hist(predicted_range.values, bins=20, color='skyblue', edgecolor='black')
    plt.title('Histogram of Predicted Ranges')
    plt.xlabel('Predicted Ranges')
    plt.ylabel('Frequency')

    pd.DataFrame(predicted_range.values).plot(kind='density')

    plt.show()