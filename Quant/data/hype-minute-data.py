import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Download data
es_data = yf.download(tickers="ES=F", period="5d", interval="1m")
tick_data = yf.download(tickers="^TICK", period="5d", interval="1m")
trin_data = yf.download(tickers="^TRIN", period="5d", interval="1m")

# Create a figure and a set of subplots
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 10), sharex=True, gridspec_kw={'height_ratios': [3, 1, 1, 1]})

# Plot the closing price on ax1
ax1.plot(es_data.index, es_data['Close'], label='Close', color='blue')
ax1.set_title('ES=F Price, Volume, TICK, and TRIN')
ax1.set_ylabel('Price')
ax1.grid(True)

# Plot the volume on ax2
ax2.bar(es_data.index, es_data['Volume'], color='gray', width=1)
ax2.set_ylabel('Volume')
ax2.grid(True)

# Plot the TICK on ax3
ax3.plot(tick_data.index, tick_data['Close'], label='TICK', color='green')
ax3.set_ylabel('TICK')
ax3.grid(True)

# Plot the TRIN on ax4
ax4.plot(trin_data.index, trin_data['Close'], label='TRIN', color='red')
ax4.set_ylabel('TRIN')
ax4.grid(True)

# Format x-axis to show the date and time nicely
ax4.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
plt.xticks(rotation=45)

# Adjust layout
plt.tight_layout()

# Display the plot
plt.show()