import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

# Download latest data
ticker = "AAPL"
data = yf.download(ticker, start="2023-01-01", end="2025-07-05")
S0 = data["Close"].iloc[-1]

# Heston model parameters
params = {
    "v0": 0.04,
    "kappa": 2.0,
    "theta": 0.04,
    "sigma": 0.3,
    "rho": -0.7
}
r = 0.02
T = 1.0

def simulate_price_paths(S0, v0, kappa, theta, sigma, rho, T, r, steps=252, paths=50):
    dt = T / steps
    S = np.zeros((steps + 1, paths))
    v = np.zeros((steps + 1, paths))
    S[0, :] = S0
    v[0, :] = v0

    for t in range(1, steps + 1):
        z1 = np.random.normal(size=paths)
        z2 = rho * z1 + np.sqrt(1 - rho ** 2) * np.random.normal(size=paths)
        v[t, :] = np.abs(
            v[t-1, :] + kappa * (theta - v[t-1, :]) * dt +
            sigma * np.sqrt(v[t-1, :]) * np.sqrt(dt) * z2
        )
        S[t, :] = S[t-1, :] * np.exp(
            (r - 0.5 * v[t-1, :]) * dt + np.sqrt(v[t-1, :]) * np.sqrt(dt) * z1
        )

    return S

# Simulate and plot
price_paths = simulate_price_paths(S0, **params, T=T, r=r)

plt.plot(price_paths)
plt.title(f"Simulated Heston Price Paths for {ticker}")
plt.xlabel("Days")
plt.ylabel("Price")
plt.grid(True)
plt.show()
