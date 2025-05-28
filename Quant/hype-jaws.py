import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import requests
import certifi
from bs4 import BeautifulSoup

# Pulls tickers from Wikipedia
def get_sp500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = requests.get(url, verify=certifi.where())
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'id': 'constituents'})

    tickers = []
    for row in table.find_all('tr')[1:]:
        ticker = row.find_all('td')[0].text.strip().replace('.', '-')
        tickers.append(ticker)

    return tickers

# Determine if price is above 20-day MA
def is_above_20ma(ticker, start_date, end_date):
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if len(data) < 20:
            raise ValueError("Not enough data")

        close = data['Close']
        if isinstance(close, pd.DataFrame):
            close = close.iloc[:, 0]

        ma_20 = close.rolling(window=20).mean()
        close_aligned, ma_aligned = close.align(ma_20, join='inner')

        above_20ma = close_aligned > ma_aligned
        above_20ma.name = ticker

        return above_20ma

    except Exception as e:
        print(f"Failed to fetch data for {ticker}: {e}")
        return pd.Series(dtype='bool')

if __name__ == "__main__":
    start_date = '2020-01-01'
    end_date = '2025-05-28'
    #end_date = datetime.today().strftime('%Y-%m-%d')

    sp500_tickers = get_sp500_tickers()
    print(f"Fetched {len(sp500_tickers)} tickers")

    all_above_20ma = []
    valid_tickers = []

    for ticker in sp500_tickers:
        above_20ma_series = is_above_20ma(ticker, start_date, end_date)
        if not above_20ma_series.empty:
            all_above_20ma.append(above_20ma_series)
            valid_tickers.append(ticker)

    if all_above_20ma:
        results = pd.concat(all_above_20ma, axis=1)
        results.columns = valid_tickers
        results['Percentage_Above_20ma'] = results.mean(axis=1) * 100
        results.dropna(inplace=True)

        # Fetch SPX index data
        spx_data = yf.download('^GSPC', start=start_date, end=end_date)

        # Extract Close price as a DataFrame with explicit column name
        if 'Close' in spx_data.columns:
            spx_close = spx_data['Close']
        elif isinstance(spx_data.columns, pd.MultiIndex):
            spx_close = spx_data['Close', '']
        else:
            raise ValueError("Could not find 'Close' column in SPX data")

        spx_close_df = pd.DataFrame(spx_close)
        spx_close_df.columns = ['SPX_Close']

        combined_data = pd.concat(
            [results['Percentage_Above_20ma'], spx_close_df],
            axis=1
        ).dropna()

        print("Columns after concat:", combined_data.columns)  # Debug print

        # Plotting
        fig, ax1 = plt.subplots(figsize=(14, 7))
        ax1.set_xlabel('Date')
        ax1.set_ylabel('% Above 20-day MA', color='b')
        ax1.plot(combined_data.index, combined_data['Percentage_Above_20ma'], label='% Above 20-day MA', color='b')
        ax1.tick_params(axis='y', labelcolor='b')

        ax2 = ax1.twinx()
        ax2.set_ylabel('S&P 500 Index (SPX)', color='r')
        ax2.plot(combined_data.index, combined_data['SPX_Close'], label='SPX Index', color='r')
        ax2.tick_params(axis='y', labelcolor='r')

        fig.tight_layout()
        plt.title('S&P 500: % Above 20-day MA vs SPX Index')
        fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
        plt.grid(True)
        plt.show()

    else:
        print("No valid data found for any ticker")
