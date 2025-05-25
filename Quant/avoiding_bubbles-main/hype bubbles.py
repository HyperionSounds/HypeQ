from lppls import lppls, data_loader
import numpy as np
import pandas as pd
from datetime import datetime as dt
import time
import yfinance as yf
import matplotlib.pyplot as plt


if __name__ == "__main__":  

    START = '2018-01-30'
    END = '2023-11-03'

    tickers = ['ES=F'] 
    adj_close_list = []
    for ticker in tickers:
        ticker_module = yf.Ticker(ticker)
        data = yf.download(ticker, start=START, end=END)
        adj_close = data['Adj Close']
        adj_close.rename(f'{ticker} Adj Close', inplace=True)
        adj_close_list.append(adj_close)

    data = data.reset_index()
    print(data)

    # convert time to ordinal
    time = [pd.Timestamp.toordinal(t1) for t1 in data['Date']]

    # create list of observation data
    price = np.log(data['Adj Close'].values)

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
    lppls_model.plot_fit()

    # should give a plot like the following...
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

    lppls_model.plot_confidence_indicators(res)
    plt.show()
    # should give a plot like the following...