import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
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

# Calculate how many are above the 20-day moving average
def is_above_20ma(ticker, start_date, end_date):
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if len(data) < 20:
            raise ValueError("Not enough data")
        data['20ma'] = data['Close'].rolling(window=20).mean()
        data['Above_20ma'] = data['Close'] > data['20ma']
        return data['Above_20ma']
    except Exception as e:
        print(f"Failed to fetch data for {ticker}: {e}")
        return pd.Series(dtype='bool')

if __name__ == "__main__":  
    
    # Define the time period
    start_date = '2020-01-01'
    end_date = datetime.today().strftime('%Y-%m-%d')

    # Fetch S&P 500 tickers
    sp500_tickers = get_sp500_tickers()
    print(f"Fetched {len(sp500_tickers)} tickers")

    # Initialize a DataFrame to hold the results
    all_above_20ma = []
    valid_tickers = []

    # Loop through the tickers and store results
    for ticker in sp500_tickers:
        above_20ma_series = is_above_20ma(ticker, start_date, end_date)
        if not above_20ma_series.empty:
            all_above_20ma.append(above_20ma_series)
            valid_tickers.append(ticker)

    # Concatenate all results into a DataFrame, aligned by date
    if all_above_20ma:
        results = pd.concat(all_above_20ma, axis=1)
        results.columns = valid_tickers

        # Calculate the percentage of stocks above the 20-day moving average
        results['Percentage_Above_20ma'] = results.mean(axis=1) * 100

        # Drop any rows with NaN values (non-trading days)
        results.dropna(inplace=True)

        # Fetch S&P 500 index data
        spx_data = yf.download('^GSPC', start=start_date, end=end_date)
        
        # Align the dates of the percentage results with SPX data
        combined_data = pd.concat([results['Percentage_Above_20ma'], spx_data['Close']], axis=1).dropna()

        # Plot the results
        fig, ax1 = plt.subplots(figsize=(14, 7))

        ax1.set_xlabel('Date')
        ax1.set_ylabel('Percentage of S&P 500 Stocks Above 20-day MA', color='b')
        ax1.plot(combined_data.index, combined_data['Percentage_Above_20ma'], label='% of S&P 500 Stocks Above 20-day MA', color='b')
        ax1.tick_params(axis='y', labelcolor='b')

        ax2 = ax1.twinx()
        ax2.set_ylabel('S&P 500 Index (SPX)', color='r')
        ax2.plot(combined_data.index, combined_data['Close'], label='S&P 500 Index (SPX)', color='r')
        ax2.tick_params(axis='y', labelcolor='r')

        fig.tight_layout()
        plt.title('Percentage of S&P 500 Stocks Above 20-day Moving Average and SPX')
        fig.legend(loc='upper left', bbox_to_anchor=(0.1,0.9))
        plt.grid(True)
        plt.show()
    else:
        print("No valid data found for any ticker")