import sqlite3
import yfinance as yf
import pandas as pd

# List of tickers to pull
tickers = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]

# Empty list to collect DataFrames
all_data = []

# Loop through tickers and collect data
for ticker in tickers:
    print(f"Downloading {ticker}...")
    df = yf.download(ticker, start="2020-01-01", end="2024-12-31")
    df.reset_index(inplace=True)
    df["ticker"] = ticker
    all_data.append(df[["ticker", "Date", "Open", "High", "Low", "Close", "Volume"]])

# Combine all into one DataFrame
full_df = pd.concat(all_data)

# Reset SQLite database and write
conn = sqlite3.connect("finance.db")
conn.execute("DROP TABLE IF EXISTS prices;")  # Optional: reset table
conn.commit()

full_df.to_sql("prices", conn, if_exists="replace", index=False)
conn.close()

print("✅ Data for all tickers saved to finance.db")
