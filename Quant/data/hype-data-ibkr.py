from ib_insync import *
import pandas as pd
import datetime as dt

# Connect to IBKR TWS or IB Gateway
# Make sure TWS/Gateway is running and API access is enabled
ib = IB()
ib.connect('127.0.0.1', 4001, clientId=1)  # port 7497 = TWS, 4001 = Gateway

def get_ibkr_ohlcv(symbol, exchange='SMART', currency='USD', start='2024-07-31', duration='1 Y', bar_size='1 day'):
    """
    symbol: ticker symbol (e.g. 'AAPL')
    exchange: exchange (usually 'SMART')
    currency: quote currency
    start: string YYYY-MM-DD
    duration: how far back to pull (e.g. '1 Y', '6 M')
    bar_size: '1 day', '1 hour', etc.
    """
    # Define the contract
    contract = Stock(symbol, exchange, currency)

    # IBKR requires duration to specify how much data to fetch.
    # endDateTime can be today
    end_dt = dt.datetime.now().strftime('%Y%m%d %H:%M:%S')

    # Fetch historical data
    bars = ib.reqHistoricalData(
        contract,
        endDateTime=end_dt,
        durationStr=duration,
        barSizeSetting=bar_size,
        whatToShow='TRADES',
        useRTH=True,        # only regular trading hours
        formatDate=1
    )

    # Convert to DataFrame
    df = util.df(bars)
    df = df.rename(columns={'date': 'Date', 'open': 'Open', 'high': 'High', 'low': 'Low',
                            'close': 'Close', 'volume': 'Volume'})
    df.set_index('Date', inplace=True)
    return df[['Open', 'High', 'Low', 'Close', 'Volume']]

# Example usage
if __name__ == '__main__':
    df = get_ibkr_ohlcv('AAPL', start='2024-07-31', duration='6 M')
    print(df.head())

# Disconnect when done
ib.disconnect()
