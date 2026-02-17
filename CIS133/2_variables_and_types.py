# ============================================================
# Assignment 2 — Variables and Types
# CIS 133 — Intro to Programming | FLLC Enterprise
# Author: Preston Furulie
# ============================================================
# Concepts: variable types (float, int, str), type conversion,
#           arithmetic expressions, formatted output, formulas
# ============================================================

# ── Step 1: Fahrenheit to Celsius Conversion ─────────────────
# Formula: C = (F - 32) × 5/9
# Source: https://www.mathsisfun.com/temperature-conversion.html

# float() ensures we handle decimal temperatures properly
fahrenheit = float(input("Enter temperature in Fahrenheit: "))

# Apply the conversion formula
# Parentheses control order of operations: subtract 32 first, then multiply
celsius = (fahrenheit - 32) * 5 / 9

# Display the result with the original input for context
print(f"  {fahrenheit}°F = {celsius:.2f}°C")

# Blank line for readability between the two conversions
print()

# ── Step 2: Celsius to Fahrenheit Conversion ─────────────────
# Formula: F = (C × 9/5) + 32

celsius = float(input("Enter temperature in Celsius: "))

# Apply the inverse formula
fahrenheit = (celsius * 9 / 5) + 32

print(f"  {celsius}°C = {fahrenheit:.2f}°F")

# ── Extended Concepts ────────────────────────────────────────
# Additional temperature conversions and variable type demonstrations

print("\n--- Reference Temperature Table ---")
print(f"  {'Description':<25} {'°F':>8} {'°C':>8} {'K':>8}")
print(f"  {'─' * 51}")

# Common reference temperatures stored as tuples (name, fahrenheit)
references = [
    ("Absolute zero",         -459.67),
    ("Water freezes",           32.00),
    ("Room temperature",        72.00),
    ("Body temperature",        98.60),
    ("Water boils",            212.00),
    ("Oven (baking)",          350.00),
    ("Surface of the Sun",  9941.00),
]

for name, f in references:
    c = (f - 32) * 5 / 9
    k = c + 273.15  # Kelvin = Celsius + 273.15
    print(f"  {name:<25} {f:>8.1f} {c:>8.1f} {k:>8.1f}")

# Variable type demonstration
print("\n--- Variable Types Used ---")
temp_int = 72
temp_float = 72.0
temp_str = "72 degrees"
temp_bool = True  # Is it hot?

print(f"  int:   {temp_int!r:<20} → type: {type(temp_int).__name__}")
print(f"  float: {temp_float!r:<20} → type: {type(temp_float).__name__}")
print(f"  str:   {temp_str!r:<20} → type: {type(temp_str).__name__}")
print(f"  bool:  {temp_bool!r:<20} → type: {type(temp_bool).__name__}")

# Type conversion chain
print("\n--- Type Conversion ---")
original = "98.6"
as_float = float(original)
as_int = int(as_float)
back_to_str = str(as_int)
print(f"  str '{original}' → float {as_float} → int {as_int} → str '{back_to_str}'")
