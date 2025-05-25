from lppls import lppls, data_loader
import numpy as np
import pandas as pd
from datetime import datetime as dt
from datetime import datetime
import yfinance as yf
import matplotlib.pyplot as plt


# Define the start and end dates
START = '2020-01-01'
END = '2025-05-24'

# Define the tickers
TICKERS = ['ES=F','NQ=F']

# Download the close prices for the tickers
close_list = []

def analyze_ticker(ticker):
    data = yf.download(ticker, start=START, end=END)  # Ensure flat columns
    print(data)
    close = data['Close']
    close_list.append(close)

    data = data.reset_index()
    print(data)

    # LPPLS model stuff:

    # convert time to ordinal
    time = np.array([pd.Timestamp.toordinal(t1) for t1 in data['Date']])

    # create list of observation data
    price = np.log(data['Close'].values).flatten()

    # create observations array (expected format for LPPLS observations)
    observations = np.array([time, price])

    # set the max number for searches to perform before giving-up
    # the literature suggests 25
    MAX_SEARCHES = 25

    # instantiate a new LPPLS model with the Nasdaq Dot-com bubble dataset
    lppls_model = lppls.LPPLS(observations=observations)

    # fit the model to the data and get back the params
    tc, m, w, a, b, c, c1, c2, O, D = lppls_model.fit(MAX_SEARCHES)


    # visualize the fit
    #plt.figure()
    lppls_model.plot_fit()
    plt.title(f'{ticker} LPPLS Fit')
    plt.show()

    # should give a plot like the following...
    # PLOT 1 LPPLS MODEL CURVE



    # compute the confidence indicator
    res = lppls_model.mp_compute_nested_fits(
        workers=8,
        window_size=120, 
        smallest_window_size=30, 
        outer_increment=1, 
        inner_increment=5, 
        max_searches=25,
        # filter_conditions_config={} # not implemented in 0.6.x
    )

     # visualize the fit
    #plt.figure()
    lppls_model.plot_confidence_indicators(res)
    plt.show()
    # should give a plot like the following...
    # PLOT 2 BUBBLE INDICATOR

def main():
    print('LPPLS analysis:')
    for ticker in TICKERS:
        analyze_ticker(ticker)
    print("Analysis complete")

if __name__ == "__main__":
    main()