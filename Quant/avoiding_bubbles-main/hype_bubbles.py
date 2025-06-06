from lppls import lppls, data_loader
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime as dt
import yfinance as yf
#%matplotlib inline


if __name__ == "__main__":  


    START = '2020-01-1'
    END = '2023-12-15'
    LOOKBACK = 21 * 6 # 21 days in a trading month


    # read example dataset into df 
    data = data_loader.nasdaq_dotcom()

    print(data)

    # convert time to ordinal
    time = [pd.Timestamp.toordinal(dt.strptime(t1, '%Y-%m-%d')) for t1 in data['Date']]

    print(data)

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
    # should give a plot like the following...

if __name__ == "__main__":
    main()