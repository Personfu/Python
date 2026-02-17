# ============================================================
# Assignment 4 — Are You Old Enough To See The Movie?
# CIS 133 — Intro to Programming | FLLC Enterprise
# Author: Preston Furulie
# ============================================================
# Concepts: if/elif/else branching, comparison operators,
#           boolean logic, functions, formatted output
# ============================================================
# Requirements:
#   - John (15) → cannot see the movie
#   - Sam (18)  → charged $15
#   - Bob (67)  → charged $5 (senior discount: $10 off)
#   - Senior citizens (65+) receive $10 discount
# ============================================================

# Define constants for pricing
TICKET_PRICE = 15       # Standard adult ticket price in dollars
SENIOR_DISCOUNT = 10    # Discount for ages 65 and over
MIN_AGE = 18            # Minimum age to see the movie
SENIOR_AGE = 65         # Age threshold for senior citizen discount

print("=" * 60)
print("  MOVIE AGE CHECK — Preston Furulie")
print("=" * 60)


# ── Helper Function ──────────────────────────────────────────
# Encapsulate the pricing logic into a reusable function

def check_movie_eligibility(name, age):
    """Determine if a person can see the movie and calculate their ticket price.

    Args:
        name: Person's name (str)
        age: Person's age in years (int)

    Returns:
        A formatted string describing the result.
    """
    if age < MIN_AGE:
        return f"  {name} is {age} years old and cannot see the movie."
    elif age >= SENIOR_AGE:
        price = TICKET_PRICE - SENIOR_DISCOUNT
        return (f"  {name} is {age} years old and will be charged ${price}."
                f"\n    (Senior discount: ${SENIOR_DISCOUNT} off ${TICKET_PRICE})")
    else:
        return f"  {name} is {age} years old and will be charged ${TICKET_PRICE}."


# ── John (Age 15) ────────────────────────────────────────────
# John is under 18, so he cannot see the movie
print(f"\n--- John ---")
print(check_movie_eligibility("John", 15))

# ── Sam (Age 18) ─────────────────────────────────────────────
# Sam is exactly 18, qualifies for standard adult pricing ($15)
print(f"\n--- Sam ---")
print(check_movie_eligibility("Sam", 18))

# ── Bob (Age 67) ─────────────────────────────────────────────
# Bob is 67, qualifies for senior citizen discount ($15 - $10 = $5)
print(f"\n--- Bob ---")
print(check_movie_eligibility("Bob", 67))


# ── Extended: Full Theater Simulation ────────────────────────
print(f"\n{'─' * 60}")
print(f"  Extended: Theater Group Pricing")
print(f"{'─' * 60}")

# A larger group visiting the theater
theater_group = [
    ("Alice", 12),
    ("Ben", 17),
    ("Carol", 21),
    ("Dave", 35),
    ("Eve", 64),
    ("Frank", 65),
    ("Grace", 78),
    ("Hank", 5),
]

total_revenue = 0
admitted = 0
denied = 0

print(f"\n  {'Name':<10} {'Age':>4}  {'Status':<12} {'Price':>6}")
print(f"  {'─' * 40}")

for name, age in theater_group:
    if age < MIN_AGE:
        status = "DENIED"
        price = 0
        denied += 1
    elif age >= SENIOR_AGE:
        status = "SENIOR"
        price = TICKET_PRICE - SENIOR_DISCOUNT
        admitted += 1
        total_revenue += price
    else:
        status = "ADMITTED"
        price = TICKET_PRICE
        admitted += 1
        total_revenue += price

    price_str = f"${price}" if price > 0 else "—"
    print(f"  {name:<10} {age:>4}  {status:<12} {price_str:>6}")

print(f"\n  Summary:")
print(f"    Admitted: {admitted}")
print(f"    Denied:   {denied}")
print(f"    Revenue:  ${total_revenue}")

# ── Branching Logic Reference ────────────────────────────────
print(f"\n{'─' * 60}")
print(f"  Pricing Rules")
print(f"{'─' * 60}")
print(f"  Age < {MIN_AGE}:  Cannot see the movie")
print(f"  Age {MIN_AGE}-{SENIOR_AGE - 1}: Standard ticket — ${TICKET_PRICE}")
print(f"  Age {SENIOR_AGE}+:  Senior ticket — ${TICKET_PRICE - SENIOR_DISCOUNT} (${SENIOR_DISCOUNT} discount)")
