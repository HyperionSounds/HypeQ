def mortgage_calculator():
    print("Mortgage Calculator")
    
    # User inputs
    home_price = float(input("Enter the home price ($): "))
    down_payment = float(input("Enter your down payment ($): "))
    annual_interest_rate = float(input("Enter the annual interest rate (e.g., 6.5 for 6.5%): "))
    loan_term_years = int(input("Enter the length of the mortgage (in years): "))
    
    # Calculated values
    loan_amount = home_price - down_payment
    monthly_interest_rate = annual_interest_rate / 100 / 12
    number_of_payments = loan_term_years * 12

    if monthly_interest_rate == 0:
        # No interest loan
        monthly_payment = loan_amount / number_of_payments
    else:
        # Monthly payment formula
        monthly_payment = loan_amount * (
            monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments
        ) / (
            (1 + monthly_interest_rate) ** number_of_payments - 1
        )
    
    # Output
    print(f"\nLoan amount: ${loan_amount:,.2f}")
    print(f"Monthly mortgage payment: ${monthly_payment:,.2f}")
    print(f"Total payment over {loan_term_years} years: ${monthly_payment * number_of_payments:,.2f}")

# Run the calculator
mortgage_calculator()
