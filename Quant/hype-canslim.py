import yfinance as yf
import pandas as pd
import datetime
import requests
from bs4 import BeautifulSoup
import certifi

# -------------------------------
# Get S&P 500 tickers from Wikipedia
# -------------------------------
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

# -------------------------------
# CANSLIM Screener
# -------------------------------
def canslim_screen(tickers):
    today = datetime.date.today()
    one_year_ago = today - datetime.timedelta(days=365)
    results = []

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            if not info or 'shortName' not in info:
                continue

            # EPS Growth (C & A)
            eps = info.get('trailingEps', 0)
            fwd_eps = info.get('forwardEps', 0)
            eps_growth = ((fwd_eps - eps) / eps * 100) if eps > 0 else 0

            # Price performance (L)
            hist = stock.history(start=one_year_ago, end=today)
            if hist.empty or len(hist) < 2:
                continue
            price_return = (hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0] * 100

            # Volume activity (S)
            avg_volume = info.get('averageVolume', 0)
            current_volume = hist['Volume'].iloc[-1]
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 0

            # Apply CANSLIM filters
            if eps_growth > 25 and price_return > 25 and volume_ratio > 1.2:
                results.append({
                    'Ticker': ticker,
                    'Company': info.get('shortName', ''),
                    'EPS Growth (%)': round(eps_growth, 2),
                    '1Y Return (%)': round(price_return, 2),
                    'Volume Ratio': round(volume_ratio, 2)
                })

        except Exception as e:
            print(f"Error processing {ticker}: {e}")

    return pd.DataFrame(results)

# -------------------------------
# Run Screener
# -------------------------------
if __name__ == "__main__":
    print("Fetching S&P 500 tickers...")
    tickers = get_sp500_tickers()
    print(f"Retrieved {len(tickers)} tickers.")

    print("Running CANSLIM filter...")
    df = canslim_screen(tickers)

    if not df.empty:
        print("\n=== CANSLIM Filtered Stocks ===")
        print(df.sort_values(by='1Y Return (%)', ascending=False))
        # Optional: save to CSV
        df.to_csv("canslim_screen_results.csv", index=False)
    else:
        print("\nNo stocks passed the CANSLIM filter criteria.")
