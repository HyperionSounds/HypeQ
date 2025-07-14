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
    ticker = 'SPY'
    vix_ticker = '^VIX'

    # Rolling window
    n = 3  # <--- change this to set how many past/future days to use

    # Download SPY data
    data = yf.download(ticker, start=START, end=END)
    mkt_data = data

    # Core return and volatility columns
    mkt_data['Return_1d'] = mkt_data['Close'].pct_change()
    mkt_data['LogReturn_1d'] = np.log(mkt_data['Close'] / mkt_data['Close'].shift(1))
    
    # n-day past rolling features
    mkt_data['Range_nd'] = mkt_data['High'].rolling(n).max() - mkt_data['Low'].rolling(n).min()
    mkt_data['Volatility_nd'] = mkt_data['LogReturn_1d'].rolling(n).std() * np.sqrt(n)
    mkt_data['PastReturn_nd'] = mkt_data['Close'].pct_change(periods=n)

    # n-day forward return (what we want to predict)
    mkt_data['FutReturn_nd'] = mkt_data['Close'].shift(-n) / mkt_data['Close'] - 1

    # Optional: Implied Vol and VRP
    vix = yf.download(vix_ticker, start=START, end=END)[['Open']]
    vix.index = vix.index.tz_localize(None)
    vix.rename(columns={'Open': 'ImpliedVol'}, inplace=True)
    mkt_data = mkt_data.join(vix, how='left')
    #mkt_data['VRP'] = mkt_data['ImpliedVol'].rank(pct=True) - mkt_data['Volatility_nd'].rank(pct=True)


    # Ensure both are Series (not accidentally DataFrames)
    iv = mkt_data['ImpliedVol']
    rv = mkt_data['Volatility_nd']

    # If either is a DataFrame (e.g. from accidental multi-column join), grab the first column
    if isinstance(iv, pd.DataFrame):
        iv = iv.iloc[:, 0]
    if isinstance(rv, pd.DataFrame):
        rv = rv.iloc[:, 0]

    # Now assign VRP safely
    mkt_data['VRP'] = iv.rank(pct=True) - rv.rank(pct=True)

    # Drop rows with NaN due to rolling or shift
    mkt_data.dropna(inplace=True)

    # -- Similarity Matching --
    # Get most recent n-day period features
    recent_range = mkt_data['Range_nd'].iloc[-1]
    recent_vol = mkt_data['Volatility_nd'].iloc[-1]

    # Compute similarity score (Euclidean distance)
    mkt_data['Distance'] = ((mkt_data['Range_nd'] - recent_range) ** 2 + 
                            (mkt_data['Volatility_nd'] - recent_vol) ** 2) ** 0.5

    # Find N most similar past periods (excluding the last row)
    num_matches = 24
    matched_rows = mkt_data.iloc[:-n].nsmallest(num_matches, 'Distance')

    print(f"\n🔍 Matching on {n}-day range and volatility:")
    print(matched_rows[['Range_nd', 'Volatility_nd', 'FutReturn_nd']])

    # -- Prediction: distribution of n-day future returns after similar periods --
    predicted_returns = matched_rows['FutReturn_nd']

    print(f"\n📈 Predicted {n}-day future returns (from similar past setups):")
    print(predicted_returns.describe())

    # -- Plot histogram --
    sns.histplot(predicted_returns, bins=25, kde=True, color='dodgerblue', edgecolor='black')
    plt.title(f'Predicted {n}-Day Returns Based on Similar Past Periods')
    plt.xlabel(f'{n}-Day Forward Return')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.axvline(predicted_returns.mean(), color='red', linestyle='--', label='Mean')
    plt.legend()
    plt.tight_layout()
    plt.show()
