import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openbb
from pysabr import Hagan2002LognormalSABR
from pysabr import hagan_2002_lognormal_sabr as sabr
from pysabr.black import lognormal_call

symbol = "SPY"
expiration = "2026-01-16"
spy = openbb.stocks.options.chains(symbol, source="YahooFinance")

calls = spy[spy.optionType == "call"]
jan_2026_c = calls[calls.expiration == expiration].set_index("strike")
jan_2026_c["mid"] = (jan_2026_c.bid + jan_2026_c.ask) / 2

puts = spy[spy.optionType == "put"]
jan_2026_p = puts[puts.expiration == expiration].set_index("strike")
jan_2026_p["mid"] = (jan_2026_p.bid + jan_2026_p.ask) / 2

strikes = jan_2026_c.index
vols = jan_2026_c.impliedVolatility * 100

f = (
    (jan_2026_c.mid - jan_2026_p.mid)
    .dropna()
    .abs()
    .sort_values()
    .index[0]
)
t = (pd.Timestamp(expiration) - pd.Timestamp.now()).days / 365
beta = 0.5

sabr_lognormal = Hagan2002LognormalSABR(
    f=f,
    t=t,
    beta=beta
)

alpha, rho, volvol = sabr_lognormal.fit(strikes, vols)

calibrated_vols = [
    sabr.lognormal_vol(strike, f, t, alpha, beta, rho, volvol) * 100
    for strike in strikes
]

plt.plot(
    strikes, 
    calibrated_vols
)

plt.xlabel("Strike")
plt.ylabel("Volatility")
plt.title("Volatility Smile")
plt.plot(strikes, vols)
plt.show()