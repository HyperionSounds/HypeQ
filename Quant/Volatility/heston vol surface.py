import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.optimize import brentq

# === Black-Scholes call price ===
def bs_call_price(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# === Implied volatility from option price ===
def implied_vol_call(C_market, S, K, T, r):
    try:
        return brentq(lambda sigma: bs_call_price(S, K, T, r, sigma) - C_market, 1e-6, 3.0)
    except ValueError:
        return np.nan

# === Heston Monte Carlo simulation ===
def simulate_heston_iv(S0, v0, kappa, theta, sigma, rho, T, K, r, paths=1000, steps=252):
    dt = T / steps
    prices = np.zeros((paths, steps + 1))
    variances = np.zeros((paths, steps + 1))
    prices[:, 0] = S0
    variances[:, 0] = v0

    for t in range(1, steps + 1):
        z1 = np.random.normal(size=paths)
        z2 = rho * z1 + np.sqrt(1 - rho**2) * np.random.normal(size=paths)
        variances[:, t] = np.abs(
            variances[:, t-1] + kappa * (theta - variances[:, t-1]) * dt +
            sigma * np.sqrt(variances[:, t-1]) * np.sqrt(dt) * z2
        )
        prices[:, t] = prices[:, t-1] * np.exp(
            (r - 0.5 * variances[:, t-1]) * dt + np.sqrt(variances[:, t-1]) * np.sqrt(dt) * z1
        )

    final_prices = prices[:, -1]
    iv_surface = []

    for strike in K:
        payoffs = np.maximum(final_prices - strike, 0)
        option_price = np.exp(-r * T) * np.mean(payoffs)
        imp_vol = implied_vol_call(option_price, S0, strike, T, r)
        iv_surface.append(imp_vol)

    return K, iv_surface

# === Main script ===
ticker = "NVDA"
data = yf.download(ticker, start="2023-01-01", end="2025-07-04")
S0 = data["Close"].iloc[-1]

params = {
    "v0": 0.04,
    "kappa": 2.0,
    "theta": 0.04,
    "sigma": 0.3,
    "rho": -0.7
}
r = 0.02
T = 1.0
K = np.linspace(0.8 * S0, 1.2 * S0, 10)

K_vals, ivs = simulate_heston_iv(S0, **params, T=T, K=K, r=r)

# === Plot ===
plt.plot(K_vals, ivs, marker='o')
plt.title(f"Implied Volatility Surface (Heston) - {ticker}")
plt.xlabel("Strike Price")
plt.ylabel("Implied Volatility")
plt.grid(True)
plt.show()
