# FinOptix 3.0 — Streamlit GUI Version with Excel Export & Scenario Comparison

import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="FinOptix 3.0", page_icon="💡")
st.title("💡 FinOptix 3.0 — Smart Financial Optimizer")

# EMI Calculation Function
def calculate_emi(principal, annual_interest_rate, tenure_years):
    monthly_interest = annual_interest_rate / (12 * 100)
    tenure_months = tenure_years * 12
    emi = principal * monthly_interest * ((1 + monthly_interest) ** tenure_months) / (((1 + monthly_interest) ** tenure_months) - 1)
    return round(emi, 2)

# Investment Split Function
def investment_split(disposable_income, risk_profile):
    if risk_profile.lower() == "low":
        return disposable_income * 0.2, disposable_income * 0.7, disposable_income * 0.1
    elif risk_profile.lower() == "medium":
        return disposable_income * 0.4, disposable_income * 0.5, disposable_income * 0.1
    else:
        return disposable_income * 0.6, disposable_income * 0.3, disposable_income * 0.1

# SIP Return Function
def sip_return(monthly_sip, annual_return_rate, tenure_years):
    months = tenure_years * 12
    monthly_rate = annual_return_rate / (12 * 100)
    future_value = monthly_sip * (((1 + monthly_rate) ** months - 1) * (1 + monthly_rate)) / monthly_rate
    return round(future_value, 2)

# User Inputs
st.sidebar.header("User Inputs")
income = st.sidebar.number_input("Monthly Income (₹)", min_value=0.0)
expenses = st.sidebar.number_input("Monthly Expenses (₹)", min_value=0.0)
existing_emi = st.sidebar.number_input("Existing EMIs (₹)", min_value=0.0)
desired_loan = st.sidebar.number_input("Desired Loan Amount (₹)", min_value=0.0)
interest_rate = st.sidebar.slider("Base Interest Rate (%)", 5.0, 15.0, 9.0)
tenure_years = st.sidebar.slider("Loan Tenure (Years)", 1, 30, 5)
credit_score = st.sidebar.slider("Credit Score", 300, 850, 700)
risk_profile = st.sidebar.selectbox("Risk Profile", ["Low", "Medium", "High"])
inflation = st.sidebar.slider("Assumed Inflation Rate (%)", 0.0, 10.0, 6.0)
investment_goal = st.sidebar.number_input("Financial Goal (₹)", min_value=0.0)
goal_years = st.sidebar.slider("Years to Achieve Goal", 1, 30, 5)

# Scenario Dataframe for comparison
scenario_data = []

if st.button("Run FinOptix Analysis"):
    # Interest Rate Adjustment by Credit Score
    if credit_score >= 750:
        interest_rate -= 0.5
    elif credit_score < 650:
        interest_rate += 0.5

    disposable_income = income - expenses - existing_emi
    safe_emi_limit = disposable_income * 0.4
    emi = calculate_emi(desired_loan, interest_rate, tenure_years)

    st.subheader("Loan Analysis")
    st.write(f"**Calculated EMI:** ₹{emi}")
    st.write(f"**Safe EMI Limit:** ₹{round(safe_emi_limit, 2)}")

    if emi <= safe_emi_limit:
        st.success("✅ Eligible for this loan.")
    else:
        st.warning("⚠️ Not eligible. Consider reducing amount or increasing tenure.")

    fd_safe, sip_equity, emergency = investment_split(disposable_income, risk_profile)

    st.subheader("Investment Suggestion")
    st.write(f"- FD/Safe: ₹{round(fd_safe, 2)}")
    st.write(f"- SIP/Equity: ₹{round(sip_equity, 2)}")
    st.write(f"- Emergency Fund: ₹{round(emergency, 2)}")

    future_value = sip_return(sip_equity, 12, goal_years)
    inflation_adjusted = future_value / ((1 + (inflation/100)) ** goal_years)

    st.subheader("SIP Future Value")
    st.write(f"- Before Inflation: ₹{future_value}")
    st.write(f"- After Inflation: ₹{round(inflation_adjusted, 2)}")

    if inflation_adjusted >= investment_goal:
        st.success("✅ You are on track to achieve your financial goal.")
    else:
        st.warning("⚠️ Increase SIP or extend goal timeline.")

    # Scenario for Export
    scenario_data.append({
        "Income": income,
        "Expenses": expenses,
        "Loan Amount": desired_loan,
        "Interest Rate": interest_rate,
        "EMI": emi,
        "Safe EMI Limit": safe_emi_limit,
        "Eligible": emi <= safe_emi_limit,
        "SIP Equity": sip_equity,
        "Future Value": future_value,
        "Inflation Adjusted Value": round(inflation_adjusted, 2),
        "Goal": investment_goal,
        "Goal Achieved": inflation_adjusted >= investment_goal
    })

    df = pd.DataFrame(scenario_data)
    st.download_button("📥 Download Scenario as CSV", df.to_csv(index=False), "FinOptix_Scenario.csv")

st.sidebar.info("Fill details & click 'Run FinOptix Analysis' to get results.")
