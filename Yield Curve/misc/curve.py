import matplotlib
import matplotlib.pyplot as plt
import io, base64, os, json, re
import pandas as pd
import numpy as np
import datetime

"""
# load data you donwloaded from Yahoo Finance
#gspc_df = pd.read_csv('^GSPC.csv') #SP500
#gspc_df['Date'] = pd.to_datetime(gspc_df['Date'])


# gotta go download data here: https://data.nasdaq.com/data/USTREASURY/YIELD-treasury-yield-curve-rates
# the data is kind of shitty
rates_df = pd.read_csv('USTREASURY-YIELD.csv')
rates_df['Date'] = pd.to_datetime(rates_df['Date'])
print(rates_df.head())
"""

# download rates.csv from ust folder package.
rates_df = pd.read_csv('rates.csv')
rates_df.columns = ['date', '1M', '3M', '6M', '1Y', '2Y', '3Y', '5Y', '7Y', '10Y', '20Y', '30Y', '30Y Display']

recent_rates = rates_df.tail

df = recent_rates
print(df)
