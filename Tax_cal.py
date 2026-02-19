import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Tax Calculator", layout="centered")
st.title("💰 Tax Calculator Web App")
st.caption("Comparison: Old vs New vs Flat Tax (includes 4% cess)")

income = st.number_input("Enter Annual Income (₹):", min_value=0.0, step=50000.0)

CESS_RATE = 0.04
FLAT_TAX_RATE = 0.20

def old_regime_tax(x: float) -> float:
    tax = 0.0
    if x <= 250000:
        tax = 0.0
    elif x <= 500000:
        tax = (x - 250000) * 0.05
    elif x <= 1000000:
        tax = (250000 * 0.05) + (x - 500000) * 0.20
    else:
        tax = (250000 * 0.05) + (500000 * 0.20) + (x - 1000000) * 0.30
    return tax * (1 + CESS_RATE)

def new_regime_tax(x: float) -> float:
    tax = 0.0
    if x <= 300000:
        tax = 0.0
    elif x <= 600000:
        tax = (x - 300000) * 0.05
    elif x <= 900000:
        tax = (300000 * 0.05) + (x - 600000) * 0.10
    elif x <= 1200000:
        tax = (300000 * 0.05) + (300000 * 0.10) + (x - 900000) * 0.15
    elif x <= 1500000:
        tax = (300000 * 0.05) + (300000 * 0.10) + (300000 * 0.15) + (x - 1200000) * 0.20
    else:
        tax = (300000 * 0.05) + (300000 * 0.10) + (300000 * 0.15) + (300000 * 0.20) + (x - 1500000) * 0.30
    return tax * (1 + CESS_RATE)

def flat_tax(x: float) -> float:
    tax = x * FLAT_TAX_RATE
    return tax * (1 + CESS_RATE)

if income > 0:
    old_tax = old_regime_tax(income)
    new_tax = new_regime_tax(income)
    flat_tax_val = flat_tax(income)

    st.subheader(" Tax Summary")
    c1, c2, c3 = st.columns(3)
    c1.metric("Old Regime", f"₹{old_tax:,.2f}")
    c2.metric("New Regime", f"₹{new_tax:,.2f}")
    c3.metric("Flat Tax (20%)", f"₹{flat_tax_val:,.2f}")

    best_val = min(old_tax, new_tax, flat_tax_val)
    best = "Old Regime" if best_val == old_tax else ("New Regime" if best_val == new_tax else "Flat Tax")
    st.success(f" Lowest Tax Regime: **{best}**")

    # Graph data
    incomes = np.linspace(0, max(income, 1), 200)
    old_vals = np.array([old_regime_tax(i) for i in incomes])
    new_vals = np.array([new_regime_tax(i) for i in incomes])
    flat_vals = np.array([flat_tax(i) for i in incomes])

    # Graph 1
    st.subheader("Graph 1: Income vs Total Tax")
    fig1 = plt.figure()
    plt.plot(incomes, old_vals, label="Old Regime")
    plt.plot(incomes, new_vals, label="New Regime")
    plt.plot(incomes, flat_vals, label="Flat Tax")
    plt.xlabel("Income (₹)")
    plt.ylabel("Total Tax (₹)")
    plt.title("Income vs Total Tax")
    plt.legend()
    st.pyplot(fig1)

    # Graph 2
    st.subheader(" Graph 2: Income vs Effective Tax Rate")
    eff_old = np.where(incomes > 0, (old_vals / incomes) * 100, 0)
    eff_new = np.where(incomes > 0, (new_vals / incomes) * 100, 0)
    eff_flat = np.where(incomes > 0, (flat_vals / incomes) * 100, 0)

    fig2 = plt.figure()
    plt.plot(incomes, eff_old, label="Old Regime")
    plt.plot(incomes, eff_new, label="New Regime")
    plt.plot(incomes, eff_flat, label="Flat Tax")
    plt.xlabel("Income (₹)")
    plt.ylabel("Effective Tax Rate (%)")
    plt.title("Income vs Effective Tax Rate")
    plt.legend()
    st.pyplot(fig2)