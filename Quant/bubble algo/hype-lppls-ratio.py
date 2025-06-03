from lppls import lppls, data_loader
import numpy as np
import pandas as pd
from datetime import datetime as dt
from datetime import datetime
import yfinance as yf
import matplotlib.pyplot as plt


# Define the start and end dates
START = '2020-01-01'
END = '2025-06-03'

# Define the tickers
#TICKERS = ['ES=F','NQ=F','^HGX']

# Download the close prices for the tickers
close_list = []

def analyze_ticker():
    #Fetch data for QQQ and TLT
    print('Fetching data from Yahoo! Finance')
    qqq_data = yf.download('QQQ', start=START, end=END)
    tlt_data = yf.download('TLT', start=START, end=END)

    # Combine and align QQQ and TLT closing prices by date
    combined = pd.concat([qqq_data['Close'], tlt_data['Close']], axis=1, join='inner')
    combined.columns = ['QQQ', 'TLT']
    combined.dropna(inplace=True)

    # Calculate QQQ/TLT ratio
    combined['QQQ_TLT_Ratio'] = combined['QQQ'] / combined['TLT']


    # Reset index to get 'Date' column
    combined = combined.reset_index()
    print(combined)

    # Convert time to ordinal
    time = [pd.Timestamp.toordinal(t1) for t1 in combined['Date']]

    # Take log of the ratio
    price = np.log(combined['QQQ_TLT_Ratio'].values).flatten()

    # Create observations array (expected format for LPPLS observations)
    observations = np.array([time, price])

    # Set max number of searches
    MAX_SEARCHES = 25

    # Instantiate LPPLS model with the dataset
    lppls_model = lppls.LPPLS(observations=observations)

    # Fit the model to the data
    tc, m, w, a, b, c, c1, c2, O, D = lppls_model.fit(MAX_SEARCHES)

    # Visualize the fit
    lppls_model.plot_fit()

    # Compute the confidence indicator
    res = lppls_model.mp_compute_nested_fits(
        workers=8,
        window_size=120, 
        smallest_window_size=30, 
        outer_increment=1, 
        inner_increment=5, 
        max_searches=25,
    )

    # Plot confidence indicators
    lppls_model.plot_confidence_indicators(res)
    plt.show()

def main():
    print('LPPLS analysis:')
    analyze_ticker()
    print("Analysis complete")

if __name__ == "__main__":
    main()