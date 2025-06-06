from lppls import lppls, data_loader
import numpy as np
import pandas as pd
from datetime import datetime as dt, timedelta
import matplotlib.pyplot as plt

if __name__ == "__main__":  

    # read example dataset into df 
    data = data_loader.nasdaq_dotcom()

    # Convert 'Date' to datetime format
    data['Date'] = pd.to_datetime(data['Date'])

    # Filter to only keep the most recent 4 years of data
    latest_date = data['Date'].max()
    four_years_ago = latest_date - pd.DateOffset(years=4)
    data = data[data['Date'] >= four_years_ago]

    # convert time to ordinal
    time = [pd.Timestamp.toordinal(t1) for t1 in data['Date']]

    # create list of observation data
    price = np.log(data['Adj Close'].values)

    # create observations array (expected format for LPPLS observations)
    observations = np.array([time, price])

    # set the max number for searches to perform before giving-up
    MAX_SEARCHES = 25

    # instantiate a new LPPLS model with the filtered dataset
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
    )

    lppls_model.plot_confidence_indicators(res)
    plt.show()