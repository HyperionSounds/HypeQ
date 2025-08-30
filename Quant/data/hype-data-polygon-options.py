import requests
import pandas as pd

# -----------------------------
# Configuration
# -----------------------------
API_KEY = "VPW919sxTSkgKfvBveVePscFxExszmHt"  # replace with your Polygon.io API key
SYMBOL = "AAPL"                   # underlying stock symbol
EXPIRATION = "2025-09-20"         # expiration date (YYYY-MM-DD)
OPTION_TYPE = "call"               # 'call' or 'put'

# -----------------------------
# Endpoint
# -----------------------------
url = f"https://api.polygon.io/v3/reference/options/contracts?underlying_ticker={SYMBOL}&expiration_date={EXPIRATION}&type={OPTION_TYPE}&limit=100&apiKey={API_KEY}"

# -----------------------------
# Request
# -----------------------------
response = requests.get(url)

if response.status_code != 200:
    print("Error:", response.status_code, response.text)
else:
    data = response.json()
    options = data.get("results", [])

    print(data)
    
    # Convert to DataFrame for easier viewing
    df = pd.DataFrame(options)
    print(df.head())
