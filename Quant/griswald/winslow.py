import numpy as np
import pandas as pd
from datetime import timedelta
import datetime as dt
import time
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns

atrLength = 20
RangeDays = 24
mkt_open = 6270

def get_next_trading_days(mkt_data, selected_rows):
    def next_trading_day_index(current_index):
        next_index = current_index + pd.DateOffset(days=1)
        while next_index.weekday() >= 5:  # Skip weekends
            next_index += pd.DateOffset(days=1)
        return next_index

    next_days_data = pd.DataFrame()
    for idx in selected_rows.index:
        next_trading_day = next_trading_day_index(idx)
        if next_trading_day in mkt_data.index:
            next_day_data = mkt_data.loc[next_trading_day]
            next_days_data = pd.concat([next_days_data, next_day_data.to_frame().T])
    return next_days_data

if __name__ == "__main__":  
    START = '2022-01-01'
    END = '2025-07-14'

    tickers = ['SPY']
    ticker = tickers[0]
    data = yf.download(ticker, start=START, end=END)
    mkt_data = data
    print('mkt_data: ', mkt_data)

    mkt_data['Range'] = mkt_data['High'] - mkt_data['Low']
    mkt_data['Return'] = mkt_data['Close'] - mkt_data['Open']
    mkt_data['TrueRange'] = pd.concat([mkt_data['High'], mkt_data['Close'].shift()], axis=1).max(axis=1) \
                          - pd.concat([mkt_data['Low'], mkt_data['Close'].shift()], axis=1).min(axis=1)
    mkt_data['ATR'] = mkt_data['TrueRange'].rolling(window=atrLength).mean()
    mkt_data['ADR'] = mkt_data['TrueRange'].rolling(window=20).mean()

    returns = np.log(mkt_data['Close'] / mkt_data['Close'].shift(1))
    returns.fillna(0, inplace=True)

    TRADING_DAYS = 30
    volatility = returns.rolling(window=TRADING_DAYS).std() * np.sqrt(TRADING_DAYS)

    mkt_data['Returns'] = returns
    mkt_data['Volatility'] = volatility

    # Download VIX (Implied Volatility)
    vticker = '^VIX'
    imp_vol = yf.download(vticker, start=START, end=END)
    print('implied vol: ', imp_vol['Open'])

    # Align implied vol: clean timezone and join by date
    imp_vol = imp_vol[['Open']]
    imp_vol = imp_vol.rename(columns={'Open': 'ImpliedVol'})
    imp_vol.index = imp_vol.index.tz_localize(None)

    mkt_data = mkt_data.join(imp_vol, how='left')

    # VRP: Implied vol rank - realized vol rank
    # Ensure we are using Series (not accidentally DataFrames)
    iv_series = mkt_data['ImpliedVol']
    rv_series = mkt_data['Volatility']

    # Check if either is actually a DataFrame (which causes this error)
    if isinstance(iv_series, pd.DataFrame) or isinstance(rv_series, pd.DataFrame):
        print("Warning: One of the volatility series is a DataFrame. Fixing...")

        # If somehow duplicated from join, try taking the first column
        if isinstance(iv_series, pd.DataFrame):
            iv_series = iv_series.iloc[:, 0]
        if isinstance(rv_series, pd.DataFrame):
            rv_series = rv_series.iloc[:, 0]

    # Now safely calculate VRP
    mkt_data['VRP'] = iv_series.rank(pct=True) - rv_series.rank(pct=True)

    print('VRP: ', mkt_data['VRP'].tail(15))

    # Drop missing values before covariance calculation
    clean_data = mkt_data[['ImpliedVol', 'Close']].dropna()
    covariance = np.cov(clean_data['ImpliedVol'], clean_data['Close'], bias=True)[0][1]
    print('Covariance between Implied Vol and Close:', covariance)

    # Last day's return
    input_range = mkt_data['Return'].iloc[-1]
    print("range: ", input_range)

    mkt_data_range_days = mkt_data.iloc[(mkt_data['Return'] - input_range).abs().argsort()[:RangeDays]]
    print('most similar range days: ', mkt_data_range_days)

    similar_days = mkt_data.loc[mkt_data.index.intersection(mkt_data_range_days.index)]
    similar_days = similar_days[:-1]
    print('similar range days: ', similar_days)

    next_trading_days_data = get_next_trading_days(mkt_data, similar_days)
    print("Next day after days with most similar range:")
    print(next_trading_days_data)

    predicted_range = (next_trading_days_data['Return']) + mkt_open
    print('predicted range: ', predicted_range)

    df_sorted = predicted_range.sort_values()
    df_sorted.reset_index(drop=True, inplace=True)
    print(df_sorted)

    sns.histplot(predicted_range.values, bins=50, kde=True, color='skyblue', edgecolor='black')
    plt.title('Histogram of Predicted Ranges')
    plt.xlabel('Predicted Ranges')
    plt.ylabel('Frequency')
    plt.show()
