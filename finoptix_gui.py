# FinOptix 3.0 — Ultimate Advanced Version with Optimized Investment, Suggestions & Full Financial Summary (Emergency Fund Fixed)

import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="FinOptix 3.0 - Ultimate", page_icon="💡")
st.title("💡 FinOptix 3.0 — Ultimate Smart Financial Optimizer")

# EMI Calculation Function
def calculate_emi(principal, annual_interest_rate, tenure_years):
    monthly_interest = annual_interest_rate / (12 * 100)
    tenure_months = tenure_years * 12
    emi = principal * monthly_interest * ((1 + monthly_interest) ** tenure_months) / (((1 + monthly_interest) ** tenure_months) - 1)
    emi = round(emi / 100) * 100  # Round EMI to nearest 100
    return emi

# Total Loan Cost Function
def total_loan_cost(emi, tenure_years, processing_fee, insurance):
    processing_fee = processing_fee if processing_fee else 0
    insurance = insurance if insurance else 0
    return round(emi * tenure_years * 12 + processing_fee + insurance, 2)

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
    future_value = round(future_value / 1000) * 1000  # Round to nearest 1000
    return future_value

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
processing_fee = st.sidebar.number_input("Processing Fee (₹)", min_value=0.0)
insurance = st.sidebar.number_input("Loan Insurance Cost (₹)", min_value=0.0)

if st.button("Run Full FinOptix Analysis"):
    if credit_score >= 750:
        interest_rate -= 0.5
    elif credit_score < 650:
        interest_rate += 0.5

    disposable_income = income - expenses - existing_emi
    emi = calculate_emi(desired_loan, interest_rate, tenure_years)
    safe_emi_limit = disposable_income * 0.4
    loan_total_cost = total_loan_cost(emi, tenure_years, processing_fee, insurance)

    st.subheader("Loan Analysis")
    st.write(f"**Calculated EMI (Rounded to ₹100):** ₹{emi}")
    st.write(f"**Safe EMI Limit:** ₹{round(safe_emi_limit, 2)}")

    if emi <= safe_emi_limit:
        st.success("✅ Eligible for this loan.")
    else:
        st.warning("⚠️ Not eligible. Suggestions:")
        suggested_loan = round((safe_emi_limit / emi) * desired_loan / 1000) * 1000
        increased_tenure = tenure_years + 2
        better_interest = max(interest_rate - 1, 5)
        st.write(f"- Suggested Loan Amount: ₹{suggested_loan}")
        st.write(f"- Suggested Increased Tenure: {increased_tenure} years")
        st.write(f"- Suggested Negotiated Interest Rate: {better_interest}%")

    remaining_income = disposable_income - emi
    investable = remaining_income
    fd_safe, sip_equity, emergency = investment_split(investable, risk_profile)

    st.subheader("Investment Suggestion")
    st.write(f"**Remaining Income after EMI:** ₹{round(remaining_income, 2)}")
    st.write(f"- FD/Safe: ₹{round(fd_safe, 2)}")
    st.write(f"- SIP/Equity: ₹{round(sip_equity, 2)}")
    st.write(f"- Emergency Fund: ₹{round(emergency, 2)}")

    future_value = sip_return(sip_equity, 12, goal_years)
    inflation_adjusted = future_value / ((1 + (inflation/100)) ** goal_years)

    st.subheader("SIP Future Value")
    st.write(f"- Before Inflation (Rounded to ₹1000): ₹{future_value}")
    st.write(f"- After Inflation: ₹{round(inflation_adjusted, 2)}")

    st.subheader("Total Loan Cost")
    st.write(f"- Loan Amount Taken: ₹{desired_loan}")
    st.write(f"- Total Repayment (EMI * Months + Processing + Insurance): ₹{loan_total_cost}")

    st.subheader("Stress Test Scenario")
    reduced_income = income * 0.8
    new_disposable = reduced_income - expenses - existing_emi
    new_safe_emi_limit = new_disposable * 0.4
    st.write(f"- If income drops by 20%, new Safe EMI Limit: ₹{round(new_safe_emi_limit, 2)}")
    if emi <= new_safe_emi_limit:
        st.success("✅ You can still afford this loan under stress scenario.")
    else:
        st.warning("⚠️ EMI exceeds safe limit under stress scenario.")
        st.write("**Suggestions to Manage:**")
        st.write("- Reduce loan amount")
        st.write("- Increase tenure")
        st.write("- Negotiate lower interest")
        st.write("- Build larger emergency fund")

    st.write("**Interest Rate Shock Test:**")
    increased_emi_half = calculate_emi(desired_loan, interest_rate + 0.5, tenure_years)
    increased_emi_one = calculate_emi(desired_loan, interest_rate + 1, tenure_years)
    st.write(f"- If interest increases by 0.5%, new EMI: ₹{increased_emi_half}")
    st.write(f"- If interest increases by 1%, new EMI: ₹{increased_emi_one}")
    if increased_emi_one <= safe_emi_limit:
        st.success("✅ Manageable even after interest hike.")
    else:
        st.warning("⚠️ EMI may become unmanageable after interest hike.")
        st.write("**Suggestions to Manage:**")
        st.write("- Reduce loan amount")
        st.write("- Increase tenure")
        st.write("- Increase income sources")

    st.subheader("Full Financial Health Summary")
    st.write(f"- Total Monthly Income: ₹{income}")
    st.write(f"- Total Expenses: ₹{expenses}")
    st.write(f"- Existing EMIs: ₹{existing_emi}")
    st.write(f"- Loan EMI: ₹{emi}")
    st.write(f"- Disposable Income after EMI: ₹{remaining_income}")
    st.write(f"- Emergency Fund: ₹{round(emergency, 2)}")
    st.write(f"- SIP Future Value After Inflation: ₹{round(inflation_adjusted, 2)}")

    st.write("**System Recommendations:**")
    if emi > safe_emi_limit:
        st.write("- Consider reducing loan amount or increasing tenure")
    if inflation_adjusted < investment_goal:
        st.write("- Increase SIP amount or extend goal timeline")
    st.write("- Build & maintain emergency fund")
    st.write("- Explore ways to increase income")
    st.write("- Review loan structure if income stability is uncertain")

st.sidebar.info("Fill details & click 'Run Full FinOptix Analysis' to get complete suggestions.")
