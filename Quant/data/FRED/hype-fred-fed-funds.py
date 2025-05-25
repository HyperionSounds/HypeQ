import pandas_datareader as pdr

import numpy as np
from matplotlib import pyplot as plt


# https://fred.stlouisfed.org/categories/22
# Cool things to pull from FRED include:
# FEDFUNDS / MORTGAGE30US / DGS10


fred_ticker = 'FEDFUNDS'

fed_data = pdr.get_data_fred(fred_ticker)
fed_data.plot()


#plt.title('10-year Constant Maturity Yields on US Government Bonds')
plt.title('Fed Funds Rate')
plt.show()


ticker_name = '^GSPC'

ticker = pdr.DataReader(ticker_name, start='2010-1-1', data_source='yahoo')
print(ticker)