
# Define the standard movie ticket price
ticket_price = 15  # Base ticket price in dollars

# Define the senior citizen discount amount
senior_discount = 10  # Discount in dollars for ages 65 and over

# --- John's age check ---
# John is 15 years old, which is under 18
john_name = "John"
john_age = 15

# Check if John is old enough to see the movie
if john_age < 18:
    # John is under 18, so he cannot see the movie
    print(john_name, "is", john_age, "years old and cannot see the movie.")
elif john_age >= 65:
    # Senior citizen pricing
    john_price = ticket_price - senior_discount
    print(john_name, "is", john_age, "years old and will be charged $" + str(john_price) + ".")
else:
    # Standard adult pricing
    print(john_name, "is", john_age, "years old and will be charged $" + str(ticket_price) + ".")

# Blank line for readability
print()

# --- Sam's age check ---
# Sam is 18 years old, which qualifies for standard adult pricing
sam_name = "Sam"
sam_age = 18

# Check if Sam is old enough to see the movie
if sam_age < 18:
    # Under 18, cannot see the movie
    print(sam_name, "is", sam_age, "years old and cannot see the movie.")
elif sam_age >= 65:
    # Senior citizen pricing
    sam_price = ticket_price - senior_discount
    print(sam_name, "is", sam_age, "years old and will be charged $" + str(sam_price) + ".")
else:
    # Standard adult pricing - Sam is 18 so he pays $15
    print(sam_name, "is", sam_age, "years old and will be charged $" + str(ticket_price) + ".")

# Blank line for readability
print()

# --- Bob's age check ---
# Bob is 67 years old, which qualifies for the senior citizen discount
bob_name = "Bob"
bob_age = 67

# Check if Bob is old enough to see the movie
if bob_age < 18:
    # Under 18, cannot see the movie
    print(bob_name, "is", bob_age, "years old and cannot see the movie.")
elif bob_age >= 65:
    # Senior citizen pricing - Bob is 67 so he gets $10 off ($15 - $10 = $5)
    bob_price = ticket_price - senior_discount
    print(bob_name, "is", bob_age, "years old and will be charged $" + str(bob_price) + ".")
else:
    # Standard adult pricing
    print(bob_name, "is", bob_age, "years old and will be charged $" + str(ticket_price) + ".")
