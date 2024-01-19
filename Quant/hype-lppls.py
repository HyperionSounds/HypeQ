from lppls import lppls, data_loader
import numpy as np
import pandas as pd
from datetime import datetime as dt
from datetime import datetime
import yfinance as yf

#%matplotlib inline

# read example dataset into df 
#data = data_loader.nasdaq_dotcom()




# Importing data with yfinance
#ticker = '^GSPC'
#yfticker= yf.Ticker(ticker)
#data = yfticker.history(start="2004-01-01", interval="1D")
#data = data.assign(symbol=ticker)

data = yf.download('^GSPC',start='2020-1-1',end='2023-1-27')

#data['Date'] = data.index
data.reset_index(level=0, inplace=True)

#print(data)

#data['Date']= str(data['Date'])
print(data['Date'])

#data['Date'].timestamp.dt.strftime('%Y-%m-%d')

#data['Date'] = data['Date'](dt.strptime("%Y-%m-%d"))




# LPPLS model stuff:
#

# convert time to ordinal
time = [pd.Timestamp.toordinal(dt.strptime(t1, '%Y-%m-%d')) for t1 in data['Date']]

# create list of observation data
price = np.log(data['Close'].values)

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

lppls_model.plot_confidence_indicators(res)
# should give a plot like the following...
# PLOT 2 BUBBLE INDICATOR