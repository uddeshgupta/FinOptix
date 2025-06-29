# FinOptix 3.0 — Smart Financial Optimizer Full Code (Python Console Version)

# Function to calculate EMI
def calculate_emi(principal, annual_interest_rate, tenure_years):
    monthly_interest = annual_interest_rate / (12 * 100)
    tenure_months = tenure_years * 12
    emi = principal * monthly_interest * ((1 + monthly_interest) ** tenure_months) / (((1 + monthly_interest) ** tenure_months) - 1)
    return round(emi, 2)

# Function to suggest Investment Split based on risk appetite
def investment_split(disposable_income, risk_profile):
    if risk_profile.lower() == "low":
        return disposable_income * 0.2, disposable_income * 0.7, disposable_income * 0.1
    elif risk_profile.lower() == "medium":
        return disposable_income * 0.4, disposable_income * 0.5, disposable_income * 0.1
    else:
        return disposable_income * 0.6, disposable_income * 0.3, disposable_income * 0.1

# Function to calculate SIP Return
def sip_return(monthly_sip, annual_return_rate, tenure_years):
    months = tenure_years * 12
    monthly_rate = annual_return_rate / (12 * 100)
    future_value = monthly_sip * (((1 + monthly_rate) ** months - 1) * (1 + monthly_rate)) / monthly_rate
    return round(future_value, 2)

# Main Program
print("Welcome to FinOptix 3.0 — Smart Financial Optimizer\n")

income = float(input("Enter your monthly income (₹): "))
expenses = float(input("Enter your monthly expenses (₹): "))
existing_emi = float(input("Enter your existing monthly EMIs (₹): "))
desired_loan = float(input("Enter desired loan amount (₹): "))
interest_rate = float(input("Enter base annual interest rate (%): "))
tenure_years = int(input("Enter loan tenure (in years): "))
credit_score = int(input("Enter your credit score: "))
risk_profile = input("Enter your risk profile (Low/Medium/High): ")
inflation = float(input("Assumed annual inflation rate (%): "))
investment_goal = float(input("Enter your financial goal amount (₹): "))
goal_years = int(input("Enter years to achieve goal: "))

# Adjust interest based on credit score
if credit_score >= 750:
    interest_rate -= 0.5
elif credit_score < 650:
    interest_rate += 0.5

# Disposable Income Calculation
disposable_income = income - expenses - existing_emi
safe_emi_limit = disposable_income * 0.4
emi = calculate_emi(desired_loan, interest_rate, tenure_years)

print(f"\nCalculated EMI for ₹{desired_loan} at {interest_rate}% for {tenure_years} years: ₹{emi}")
print(f"Safe EMI Limit (40% of Disposable Income): ₹{round(safe_emi_limit, 2)}")

# Loan Eligibility Check
if emi <= safe_emi_limit:
    print("\n✅ You are eligible for this loan.")
else:
    print("\n⚠️ You are NOT eligible for this loan. Suggestions:")
    suggested_loan = (safe_emi_limit / emi) * desired_loan
    print(f"- Reduce loan amount to around ₹{round(suggested_loan, 2)}")
    print("- Increase tenure or negotiate better interest rate")

# Investment Split
fd_safe, sip_equity, emergency = investment_split(disposable_income, risk_profile)
print(f"\nRecommended Investment Split:")
print(f"- FD/Safe: ₹{round(fd_safe, 2)}")
print(f"- SIP/Equity: ₹{round(sip_equity, 2)}")
print(f"- Emergency Fund: ₹{round(emergency, 2)}")

# SIP Return Calculation
future_value = sip_return(sip_equity, 12, goal_years)
inflation_adjusted = future_value / ((1 + (inflation/100)) ** goal_years)
print(f"\nEstimated SIP Future Value (before inflation): ₹{future_value}")
print(f"Estimated SIP Future Value (after inflation): ₹{round(inflation_adjusted, 2)}")

# Goal Tracking
if inflation_adjusted >= investment_goal:
    print("✅ You are on track to achieve your financial goal.")
else:
    print("⚠️ You may need to increase your SIP or extend your goal timeline.")

print("\nThank you for using FinOptix 3.0!")
