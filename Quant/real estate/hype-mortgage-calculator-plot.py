import matplotlib.pyplot as plt

def mortgage_calculator():
    print("Mortgage Calculator with Overpayment and Full Visualization")
    
    # User inputs
    home_price = float(input("Enter the home price ($): "))
    down_payment = float(input("Enter your down payment ($): "))
    annual_interest_rate = float(input("Enter the annual interest rate (e.g., 6.5 for 6.5%): "))
    loan_term_years = int(input("Enter the length of the mortgage (in years): "))
    overpayment = float(input("Enter your chosen monthly payment (overpayment allowed): "))

    # Derived values
    loan_amount = home_price - down_payment
    monthly_interest_rate = annual_interest_rate / 100 / 12
    total_months = loan_term_years * 12

    # Standard monthly payment
    if monthly_interest_rate == 0:
        standard_monthly = loan_amount / total_months
    else:
        standard_monthly = loan_amount * (
            monthly_interest_rate * (1 + monthly_interest_rate) ** total_months
        ) / (
            (1 + monthly_interest_rate) ** total_months - 1
        )

    # Amortization schedule for standard payment
    balance_std = loan_amount
    interest_paid_std = 0
    balance_history_std = []
    principal_paid_std = []
    interest_cumulative_std = []

    for _ in range(total_months):
        interest = balance_std * monthly_interest_rate
        principal = standard_monthly - interest
        balance_std -= principal
        interest_paid_std += interest
        balance_history_std.append(balance_std if balance_std > 0 else 0)
        principal_paid_std.append(loan_amount - balance_std)
        interest_cumulative_std.append(interest_paid_std)

    # Amortization with overpayment
    balance_ovp = loan_amount
    interest_paid_ovp = 0
    month = 0
    balance_history_ovp = []
    principal_paid_ovp = []
    interest_cumulative_ovp = []

    while balance_ovp > 0:
        interest = balance_ovp * monthly_interest_rate
        principal = overpayment - interest
        if principal <= 0:
            print("Overpayment too low to reduce balance. Try a higher amount.")
            return
        balance_ovp -= principal
        interest_paid_ovp += interest
        balance_history_ovp.append(balance_ovp if balance_ovp > 0 else 0)
        principal_paid_ovp.append(loan_amount - balance_ovp)
        interest_cumulative_ovp.append(interest_paid_ovp)
        month += 1

    # Results
    print(f"\n--- Results ---")
    print(f"Loan amount: ${loan_amount:,.2f}")
    print(f"Standard monthly payment: ${standard_monthly:,.2f}")
    print(f"Overpayment monthly: ${overpayment:,.2f}")
    print(f"\nWith standard payment:")
    print(f" - Total interest paid: ${interest_paid_std:,.2f}")
    print(f" - Loan term: {loan_term_years} years ({total_months} months)")
    print(f"\nWith overpayment:")
    print(f" - Total interest paid: ${interest_paid_ovp:,.2f}")
    print(f" - Months to repay: {month} ({month // 12} years and {month % 12} months)")
    print(f" - Interest saved: ${interest_paid_std - interest_paid_ovp:,.2f}")

    # Plotting
    plt.figure(figsize=(14, 8))

    # Mortgage Balance
    plt.subplot(3, 1, 1)
    plt.plot(range(total_months), balance_history_std, label="Balance (Standard)", color='blue')
    plt.plot(range(month), balance_history_ovp, label="Balance (Overpayment)", color='red')
    plt.ylabel("Balance ($)")
    plt.title("Mortgage Balance Over Time")
    plt.legend()
    plt.grid(True)

    # Principal Paid
    plt.subplot(3, 1, 2)
    plt.plot(range(total_months), principal_paid_std, label="Principal Paid (Standard)", color='blue', linestyle='--')
    plt.plot(range(month), principal_paid_ovp, label="Principal Paid (Overpayment)", color='red', linestyle='--')
    plt.ylabel("Principal Paid ($)")
    plt.title("Cumulative Principal Paid")
    plt.legend()
    plt.grid(True)

    # Interest Paid
    plt.subplot(3, 1, 3)
    plt.plot(range(total_months), interest_cumulative_std, label="Interest Paid (Standard)", color='blue')
    plt.plot(range(month), interest_cumulative_ovp, label="Interest Paid (Overpayment)", color='red')
    plt.xlabel("Month")
    plt.ylabel("Interest Paid ($)")
    plt.title("Cumulative Interest Paid")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# Run
mortgage_calculator()