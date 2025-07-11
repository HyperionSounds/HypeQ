# Investment growth model with monthly contributions and daily compounding

# Parameters
daily_return_rate = 1.01  # 1.7% daily growth (i.e., 1.017 multiplier)
monthly_contribution = 0000  # Contribution every 30 days
target_value = 4_000_000  # Final investment goal
initial_balance = 2000 # Start from $0

# Initialize variables
balance = initial_balance
day = 0
balance_history = []

# Simulation loop
while balance < target_value:
    # Add monthly contribution every 30 days (day 0, 30, 60, ...)
    if day % 30 == 0:
        balance += monthly_contribution

    # Apply daily return
    balance *= daily_return_rate

    # Record balance for tracking (optional)
    balance_history.append(balance)

    # Advance time
    day += 1

# Output results
years = day / 365
print(f"Target reached in {day} days, or {years:.2f} years.")
