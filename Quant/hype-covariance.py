import yfinance as yf
import pandas as pd
import numpy as np

start = '20150101'
end = '20200101'

qqq = yf.Ticker('QQQ')
qqq_price = qqq.history(period='max')['Close'][start:end]
qqq_price.name = 'QQQ'

aapl = yf.Ticker('AAPL')
aapl_price = aapl.history(period='max')['Close'][start:end]
aapl_price.name = 'AAPL'

prices = pd.concat([qqq_price, aapl_price], axis=1)

def daily_returns(prices):
    res = (prices/prices.shift(1) - 1.0)[1:]
    return res

def cumulative_returns(returns):
    res = (returns + 1.0).cumprod()
    return res

cum_returns = cumulative_returns(daily_returns(prices))

res = cum_returns.copy()
res['one'] = 1.0
# res['AAPL'] = beta * res['QQQ'] + alpha
beta, alpha = np.linalg.lstsq(res[['QQQ', 'one']],
                              res['AAPL'],
                              rcond=None)[0]
print(f'{beta}, {alpha}')
# 1.296273279456101, -0.3648736136108661


cov = cum_returns.cov()
#           QQQ      AAPL
#QQQ   0.115635  0.149894
#AAPL  0.149894  0.210077


Beta = cov.iloc[0][1] / cov.iloc[0][0]
print(Beta)