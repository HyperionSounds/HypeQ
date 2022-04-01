from fredapi import Fred
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter


# FRED data - download a bunch of stuff from the FEDs website
# https://mortada.net/python-api-for-fred.html


#881bb77eb8276c4a046d970bff5b1db2
#fred = Fred(api_key='insert api key here')

fred = Fred(api_key='881bb77eb8276c4a046d970bff5b1db2')



SPX = fred.get_series('SP500')
print(SPX)

data_GDP = fred.get_series_latest_release('GDP')
print(data_GDP.tail())


# gets the money supply
M2SL_info = fred.get_series_info('M2SL')
M2SL_data = fred.get_series('M2SL', observation_start='2004-01-01', observation_end='2022-03-25')
#M2SL_data = fred.get_series_latest_release('M2SL')
print(M2SL_data)


# Pulls personal income series for locations we care about
personal_income_series = fred.search_by_release(175, limit=50, order_by='popularity', sort_order='desc')
personal_income_series['title']

print(personal_income_series['title'])

df = {}

df['NY'] = fred.get_series('PCPI36061')
df['DC'] = fred.get_series('PCPI11001')

df['SF'] = fred.get_series('PCPI06075')
df['OC'] = fred.get_series('PCPI06059')
df['SD'] = fred.get_series('PCPI06073')

df['SEA'] = fred.get_series('SEAT653PCPI')
df['DEN'] = fred.get_series('DENV708PCPI')
df['PDX'] = fred.get_series('PORT941PCPI')


df['ATX'] = fred.get_series('AUST448PCPI')
df = pd.DataFrame(df)
df.plot()

plt.title("Personal Income Series")
plt.xlabel("Time")
plt.xlim('1-1-2000', '3-30-2022')     # set the xlim to left, right
plt.ylabel("$")
plt.grid()

print('DEN: ',df['DEN'])
print('PDX: ',df['PDX'])

NFP = fred.get_series('PAYEMS')
print('NFP: ',NFP)

plt.show()