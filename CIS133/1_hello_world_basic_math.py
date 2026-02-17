# ============================================================
# Assignment 1 — Hello World & Basic Math
# CIS 133 — Intro to Programming | FLLC Enterprise
# Author: Preston Furulie
# ============================================================
# Concepts: input(), print(), float(), arithmetic operators,
#           string formatting, f-strings, basic program flow
# ============================================================

# ── Step 1: Get the user's name ──────────────────────────────
# input() reads a string from the keyboard and stores it
name = input("Enter your name: ")

# ── Step 2: Get yearly income ────────────────────────────────
# float() converts the string input to a decimal number
# so we can do arithmetic on it
yearly_salary = float(input("Enter your yearly income: "))

# ── Step 3: Calculate monthly salary ─────────────────────────
# Divide annual salary by 12 months
monthly_salary = yearly_salary / 12

# ── Step 4: Display results ──────────────────────────────────
# format(value, ".2f") rounds to 2 decimal places for currency
print("Hello", name, "your monthly salary is", format(monthly_salary, ".2f"))

# ── Extended Concepts ────────────────────────────────────────
# Demonstrate additional formatting approaches and calculations
# that build on the core assignment requirements.

# f-string formatting (modern Python approach)
print(f"\n--- Detailed Breakdown for {name} ---")
print(f"  Yearly salary:   ${yearly_salary:>12,.2f}")
print(f"  Monthly salary:  ${monthly_salary:>12,.2f}")

# Weekly and daily calculations
weekly_salary = yearly_salary / 52
daily_salary = yearly_salary / 365
hourly_rate = yearly_salary / (52 * 40)  # assuming 40-hour work weeks

print(f"  Weekly salary:   ${weekly_salary:>12,.2f}")
print(f"  Daily salary:    ${daily_salary:>12,.2f}")
print(f"  Hourly rate:     ${hourly_rate:>12,.2f}  (based on 40-hr weeks)")

# Tax estimation (simplified federal brackets for demonstration)
# These are not real tax rates — just for showing conditional math
if yearly_salary <= 11600:
    tax_rate = 0.10
elif yearly_salary <= 47150:
    tax_rate = 0.12
elif yearly_salary <= 100525:
    tax_rate = 0.22
elif yearly_salary <= 191950:
    tax_rate = 0.24
else:
    tax_rate = 0.32

estimated_tax = yearly_salary * tax_rate
net_yearly = yearly_salary - estimated_tax
net_monthly = net_yearly / 12

print(f"\n--- Estimated Tax Summary ---")
print(f"  Tax bracket:     {tax_rate:.0%}")
print(f"  Estimated tax:   ${estimated_tax:>12,.2f}")
print(f"  Net yearly:      ${net_yearly:>12,.2f}")
print(f"  Net monthly:     ${net_monthly:>12,.2f}")

# Data type demonstration
print(f"\n--- Variable Types ---")
print(f"  name            = {name!r:<30} type: {type(name).__name__}")
print(f"  yearly_salary   = {yearly_salary:<30} type: {type(yearly_salary).__name__}")
print(f"  monthly_salary  = {monthly_salary:<30} type: {type(monthly_salary).__name__}")
print(f"  tax_rate        = {tax_rate:<30} type: {type(tax_rate).__name__}")
