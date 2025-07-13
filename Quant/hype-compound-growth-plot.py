import matplotlib.pyplot as plt
import pandas as pd
from datetime import date
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay

# Parameters
daily_return_rate = 1.017  # 1.7% daily return
monthly_contribution = 1000
target_value = 4_000_000
start_date = date(2025, 1, 1)
end_date = date(2050, 1, 1)
contribution_interval = 30  # every 30 calendar days

# Generate U.S. stock market business days
us_bd = CustomBusinessDay(calendar=USFederalHolidayCalendar())
business_days = pd.date_range(start=start_date, end=end_date, freq=us_bd)

# Initialize simulation
balance = 100000
last_contribution_date = start_date
balance_history = []
date_history = []

# Simulate account growth
for current_date in business_days:
    if (current_date.date() - last_contribution_date).days >= contribution_interval:
        balance += monthly_contribution
        last_contribution_date = current_date.date()

    balance *= daily_return_rate

    balance_history.append(balance)
    date_history.append(current_date)

    if balance >= target_value:
        break

# Compute final results
total_market_days = len(balance_history)
approx_years = total_market_days / 252  # Assuming 252 trading days/year

# Print results
print(f"Reached ${target_value:,.0f} in {total_market_days} market days (~{approx_years:.2f} years)")

# Plot the results
plt.figure(figsize=(12, 6))
plt.plot(date_history, balance_history, label='Portfolio Value')
plt.axhline(y=target_value, color='red', linestyle='--', label='Target ($4M)')
plt.title('Investment Account Growth Over Time\n($2,000/month, 1.7% Market Day Returns)')
plt.xlabel('Date')
plt.ylabel('Account Balance ($)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
