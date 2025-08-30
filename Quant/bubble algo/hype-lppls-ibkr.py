from ib_insync import *
from lppls import lppls, data_loader
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Connect to IB Gateway / TWS
ib = IB()
ib.connect('127.0.0.1', 4001, clientId=1)

# Define the start and end dates
START = '2020-01-01'
END = '2025-08-27'

# Define the tickers
TICKERS = ['ES=F','NQ=F','ZN=F','SOXX','NVDA','AMD','TSLA','AAPL']

# -----------------------------
# Contract resolver
# -----------------------------
def resolve_contract(ticker):
    """
    Map a ticker to an IBKR contract.
    Futures (like ES=F) are resolved to the current front-month.
    Stocks/ETFs are mapped to SMART/USD.
    """
    futures_map = {
        'ES=F': 'ES',
        'NQ=F': 'NQ',
        'ZN=F': 'ZN'
    }

    if ticker in futures_map:
        symbol = futures_map[ticker]
        base_contract = Future(symbol, '', 'CME')  # leave expiry blank
        cds = ib.reqContractDetails(base_contract)
        if cds:
            print(f"✅ Resolved {ticker} to {cds[0].contract}")
            return cds[0].contract
        else:
            print(f"❌ Could not resolve contract for {ticker}")
            return None
    else:
        return Stock(ticker, 'SMART', 'USD')

# -----------------------------
# Data fetcher
# -----------------------------
def get_ibkr_data(contract, start, end):
    """Fetch OHLCV data from IBKR into pandas DataFrame"""
    endDateTime = ''  # empty string = "now"

    bars = ib.reqHistoricalData(
        contract,
        endDateTime=endDateTime,
        durationStr='5 Y',
        barSizeSetting='1 day',
        whatToShow='TRADES',
        useRTH=True,
        formatDate=1
    )

    if not bars:
        print(f"⚠️ No data returned for {contract}")
        return pd.DataFrame()

    df = util.df(bars)
    df = df.rename(columns={
        'date': 'Date',
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close',
        'volume': 'Volume'
    })
    df['Date'] = pd.to_datetime(df['Date'])
    df = df[(df['Date'] >= start) & (df['Date'] <= end)]
    return df.reset_index(drop=True)

# -----------------------------
# LPPLS analysis
# -----------------------------
def analyze_ticker(ticker, contract):
    print(f"\nFetching {ticker} data from IBKR...")
    data = get_ibkr_data(contract, START, END)
    if data.empty:
        print(f"❌ Skipping {ticker} — no data retrieved.")
        return

    # LPPLS model stuff
    time = np.array([pd.Timestamp.toordinal(t1) for t1 in data['Date']])
    price = np.log(data['Close'].values).flatten()
    observations = np.array([time, price])

    lppls_model = lppls.LPPLS(observations=observations)
    tc, m, w, a, b, c, c1, c2, O, D = lppls_model.fit(25)

    # visualize the fit
    lppls_model.plot_fit()
    plt.title(f'{ticker} LPPLS Fit')
    plt.show()

    # compute confidence indicator
    res = lppls_model.mp_compute_nested_fits(
        workers=8,
        window_size=120,
        smallest_window_size=30,
        outer_increment=1,
        inner_increment=5,
        max_searches=25
    )

    lppls_model.plot_confidence_indicators(res)
    plt.show()

# -----------------------------
# Main
# -----------------------------
def main():
    print('LPPLS analysis:')
    for ticker in TICKERS:
        contract = resolve_contract(ticker)
        if contract:
            analyze_ticker(ticker, contract)
    print("Analysis complete")

if __name__ == "__main__":
    main()
