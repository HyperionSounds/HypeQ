import matplotlib.pyplot as plt

def compare_mortgages():
    print("Compare Two Mortgage Scenarios")

    # Shared Inputs
    home_price = float(input("Enter the home price ($): "))
    down_payment = float(input("Enter your down payment ($): "))
    loan_term_years = int(input("Enter the loan term in years: "))
    rate1 = float(input("Enter the first interest rate (e.g., 6.5 for 6.5%): "))
    rate2 = float(input("Enter the second interest rate (e.g., 4 for 4.0%): "))

    loan_amount = home_price - down_payment
    n_months = loan_term_years * 12

    def amortize(rate):
        monthly_rate = rate / 100 / 12
        if monthly_rate == 0:
            monthly_payment = loan_amount / n_months
        else:
            monthly_payment = loan_amount * (
                monthly_rate * (1 + monthly_rate) ** n_months
            ) / (
                (1 + monthly_rate) ** n_months - 1
            )

        balance = loan_amount
        balances, principals, interests = [], [], []
        total_interest = 0

        for _ in range(n_months):
            interest = balance * monthly_rate
            principal = monthly_payment - interest
            balance -= principal
            total_interest += interest
            balances.append(balance if balance > 0 else 0)
            principals.append(loan_amount - balance)
            interests.append(total_interest)

        total_payment = monthly_payment * n_months
        return monthly_payment, balances, principals, interests, total_interest, total_payment

    # Amortize both scenarios
    result1 = amortize(rate1)
    result2 = amortize(rate2)

    # Print Comparison
    print("\n--- Comparison ---")
    print(f"Loan amount: ${loan_amount:,.2f} for {loan_term_years} years")
    print(f"\nRate: {rate1:.2f}%")
    print(f" - Monthly payment: ${result1[0]:,.2f}")
    print(f" - Total interest paid: ${result1[4]:,.2f}")
    print(f" - Total cost: ${result1[5]:,.2f}")

    print(f"\nRate: {rate2:.2f}%")
    print(f" - Monthly payment: ${result2[0]:,.2f}")
    print(f" - Total interest paid: ${result2[4]:,.2f}")
    print(f" - Total cost: ${result2[5]:,.2f}")

    print(f"\nInterest savings with {rate2:.2f}% vs {rate1:.2f}%: ${result1[4] - result2[4]:,.2f}")

    # Plotting
    months = list(range(n_months))

    plt.figure(figsize=(14, 9))

    # Balance
    plt.subplot(3, 1, 1)
    plt.plot(months, result1[1], label=f"Balance @ {rate1:.2f}%", color='blue')
    plt.plot(months, result2[1], label=f"Balance @ {rate2:.2f}%", color='green')
    plt.ylabel("Balance ($)")
    plt.title("Mortgage Balance Comparison")
    plt.grid(True)
    plt.legend()

    # Principal paid
    plt.subplot(3, 1, 2)
    plt.plot(months, result1[2], label=f"Principal @ {rate1:.2f}%", linestyle='--', color='blue')
    plt.plot(months, result2[2], label=f"Principal @ {rate2:.2f}%", linestyle='--', color='green')
    plt.ylabel("Principal Paid ($)")
    plt.title("Cumulative Principal Paid")
    plt.grid(True)
    plt.legend()

    # Interest paid
    plt.subplot(3, 1, 3)
    plt.plot(months, result1[3], label=f"Interest @ {rate1:.2f}%", linestyle='-', color='blue')
    plt.plot(months, result2[3], label=f"Interest @ {rate2:.2f}%", linestyle='-', color='green')
    plt.xlabel("Month")
    plt.ylabel("Interest Paid ($)")
    plt.title("Cumulative Interest Paid")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

# Run
compare_mortgages()
