# ============================================================
# Loops & Iteration — Complete Implementation
# CIS 133 — Intro to Programming | Preston Furulie
# ============================================================
# Covers: for loops, while loops, break/continue, enumerate,
# range() options, nested loops, pattern printing, list
# comprehensions, do-while pattern, and loop-based algorithms.
# ============================================================


# ── Section 1: For Loop Fundamentals ────────────────────────

# Basic for loop with range()
# range(stop)         → 0 to stop-1
# range(start, stop)  → start to stop-1
# range(start, stop, step) → start to stop-1, incrementing by step

print("=" * 60)
print("  LOOPS & ITERATION — CIS 133 | Preston Furulie")
print("=" * 60)

# Count from 1 to 10
print("\n--- For Loop: Counting 1-10 ---")
for i in range(1, 11):
    print(i, end=" ")
print()

# Count by 5s from 0 to 50
print("\n--- For Loop: Count by 5s ---")
for i in range(0, 51, 5):
    print(i, end=" ")
print()

# Count backwards from 10 to 1
print("\n--- For Loop: Countdown ---")
for i in range(10, 0, -1):
    print(i, end=" ")
print("\nLiftoff!")


# ── Section 2: While Loop Fundamentals ──────────────────────

# While loop runs as long as the condition is True
# Must include a way to eventually make the condition False (avoid infinite loops)

print("\n--- While Loop: Password Checker ---")
max_attempts = 3
attempts = 0
correct_password = "python123"

while attempts < max_attempts:
    password = input(f"  Enter password (attempt {attempts + 1}/{max_attempts}): ")
    if password == correct_password:
        print("  Access granted!")
        break
    else:
        attempts += 1
        remaining = max_attempts - attempts
        if remaining > 0:
            print(f"  Wrong password. {remaining} attempt(s) remaining.")
else:
    # This else block runs if the while condition becomes False
    # (i.e., the loop was NOT exited via break)
    print("  Account locked. Too many failed attempts.")


# ── Section 3: Break, Continue, and Pass ────────────────────

# break    — immediately exit the entire loop
# continue — skip the rest of this iteration, go to next
# pass     — do nothing (placeholder for future code)

print("\n--- Break: Find first multiple of 7 above 50 ---")
for num in range(51, 200):
    if num % 7 == 0:
        print(f"  Found: {num}")
        break

print("\n--- Continue: Print odd numbers only (1-20) ---")
for num in range(1, 21):
    if num % 2 == 0:
        continue  # skip even numbers
    print(num, end=" ")
print()


# ── Section 4: Enumerate and Iterating Collections ──────────

# enumerate() gives both the index and value during iteration
fruits = ["apple", "banana", "cherry", "date", "elderberry"]

print("\n--- Enumerate: Fruits with index ---")
for index, fruit in enumerate(fruits):
    print(f"  {index}: {fruit}")

# Iterating with start index
print("\n--- Enumerate: Starting at 1 ---")
for position, fruit in enumerate(fruits, start=1):
    print(f"  #{position} {fruit}")

# Iterating over a dictionary
student_grades = {
    "Preston": 95,
    "Alice": 88,
    "Bob": 72,
    "Carol": 91,
    "Dave": 67
}

print("\n--- Dictionary Iteration ---")
for name, grade in student_grades.items():
    status = "PASS" if grade >= 70 else "FAIL"
    print(f"  {name:<10} {grade:>3}  [{status}]")


# ── Section 5: Nested Loops ─────────────────────────────────

# Multiplication table (10 x 10)
print("\n--- Nested Loops: Multiplication Table (1-10) ---")
print("     ", end="")
for j in range(1, 11):
    print(f"{j:>5}", end="")
print()
print("  " + "-" * 55)

for i in range(1, 11):
    print(f"  {i:>2} |", end="")
    for j in range(1, 11):
        print(f"{i * j:>5}", end="")
    print()


# ── Section 6: Pattern Printing ─────────────────────────────

print("\n--- Right Triangle (stars) ---")
rows = 5
for i in range(1, rows + 1):
    print("  " + "* " * i)

print("\n--- Inverted Triangle ---")
for i in range(rows, 0, -1):
    print("  " + "* " * i)

print("\n--- Centered Pyramid ---")
for i in range(1, rows + 1):
    spaces = " " * (rows - i)
    stars = "* " * i
    print(f"  {spaces}{stars}")

print("\n--- Diamond ---")
for i in range(1, rows + 1):
    print("  " + " " * (rows - i) + "* " * i)
for i in range(rows - 1, 0, -1):
    print("  " + " " * (rows - i) + "* " * i)


# ── Section 7: List Comprehensions ──────────────────────────

# List comprehension: concise syntax for creating lists from loops

# Squares of 1-10
squares = [x ** 2 for x in range(1, 11)]
print(f"\n--- List Comprehension: Squares ---\n  {squares}")

# Even numbers from 1-20
evens = [x for x in range(1, 21) if x % 2 == 0]
print(f"\n--- Filtered: Evens ---\n  {evens}")

# Uppercase conversion
words = ["hello", "world", "python", "loops"]
upper_words = [w.upper() for w in words]
print(f"\n--- Transformed: Uppercase ---\n  {upper_words}")

# Nested comprehension: flatten a 2D list
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]
print(f"\n--- Flattened matrix ---\n  {matrix} → {flat}")


# ── Section 8: Practical Loop Algorithms ────────────────────

# Sum and average
numbers = [23, 45, 12, 67, 89, 34, 56, 78, 90, 11]
total = 0
count = 0
minimum = numbers[0]
maximum = numbers[0]

for n in numbers:
    total += n
    count += 1
    if n < minimum:
        minimum = n
    if n > maximum:
        maximum = n

average = total / count

print(f"\n--- Loop Statistics ---")
print(f"  Numbers: {numbers}")
print(f"  Sum:     {total}")
print(f"  Count:   {count}")
print(f"  Average: {average:.2f}")
print(f"  Min:     {minimum}")
print(f"  Max:     {maximum}")

# Fibonacci sequence using a loop
print("\n--- Fibonacci Sequence (first 15 terms) ---")
fib_count = 15
a, b = 0, 1
fib_sequence = []
for _ in range(fib_count):
    fib_sequence.append(a)
    a, b = b, a + b
print(f"  {fib_sequence}")

# Prime number checker
print("\n--- Prime Numbers (1-50) ---")
primes = []
for num in range(2, 51):
    is_prime = True
    for divisor in range(2, int(num ** 0.5) + 1):
        if num % divisor == 0:
            is_prime = False
            break
    if is_prime:
        primes.append(num)
print(f"  {primes}")

# FizzBuzz (classic interview problem)
print("\n--- FizzBuzz (1-30) ---")
for i in range(1, 31):
    if i % 15 == 0:
        print("FizzBuzz", end=" ")
    elif i % 3 == 0:
        print("Fizz", end=" ")
    elif i % 5 == 0:
        print("Buzz", end=" ")
    else:
        print(i, end=" ")
print()
