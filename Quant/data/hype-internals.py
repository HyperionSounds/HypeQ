from ib_insync import *
import pandas as pd
import datetime

# Connect to IBKR API
ib = IB()
ib.connect('127.0.0.1', 4001, clientId=1)  # 7497 is the default port for TWS; use 4001 for IB Gateway

# Define the TICK contract
tick_contract = Index(symbol='AAPL', exchange='NYSE')

# Request historical data for the last 5 days at 1-minute intervals
end_time = ''
duration = '5 D'
bar_size = '1 min'
what_to_show = 'TRADES'  # This can be adjusted as needed

# Fetch historical data
tick_bars = ib.reqHistoricalData(
    tick_contract,
    endDateTime=end_time,
    durationStr=duration,
    barSizeSetting=bar_size,
    whatToShow=what_to_show,
    useRTH=True,
    formatDate=1
)

# Convert to a Pandas DataFrame
tick_df = util.df(tick_bars)

print(tick_df)

# Save the data to a CSV file (optional)
tick_df.to_csv('tick_data.csv')

# Disconnect from IBKR
ib.disconnect()

# Print the first few rows of the data
print(tick_df.head())