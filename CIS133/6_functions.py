# ============================================================
# Functions — Complete Implementation
# CIS 133 — Intro to Programming | Preston Furulie
# ============================================================
# Covers: defining functions, parameters, return values,
# default arguments, *args, **kwargs, lambda, recursion,
# scope, docstrings, type hints, decorators, and closures.
# ============================================================

print("=" * 60)
print("  FUNCTIONS — CIS 133 | Preston Furulie")
print("=" * 60)


# ── Section 1: Basic Function Definition ────────────────────

def greet(name):
    """Greet a person by name. Demonstrates basic function syntax."""
    return f"Hello, {name}! Welcome to CIS 133."

print("\n--- Basic Function ---")
print(greet("Preston"))


# ── Section 2: Multiple Parameters and Return Values ────────

def calculate_rectangle(length, width):
    """Calculate area and perimeter of a rectangle.
    Returns a tuple of (area, perimeter)."""
    area = length * width
    perimeter = 2 * (length + width)
    return area, perimeter

print("\n--- Multiple Return Values ---")
a, p = calculate_rectangle(8, 5)
print(f"  Rectangle 8x5: area = {a}, perimeter = {p}")


def circle_properties(radius):
    """Calculate area, circumference, and diameter of a circle."""
    import math
    area = math.pi * radius ** 2
    circumference = 2 * math.pi * radius
    diameter = 2 * radius
    return {
        "radius": radius,
        "diameter": diameter,
        "area": round(area, 4),
        "circumference": round(circumference, 4)
    }

print("\n--- Dictionary Return ---")
props = circle_properties(7)
for key, value in props.items():
    print(f"  {key:<15} {value}")


# ── Section 3: Default Parameters ──────────────────────────

def power(base, exponent=2):
    """Raise base to exponent. Defaults to squaring."""
    return base ** exponent

print("\n--- Default Parameters ---")
print(f"  power(5)     = {power(5)}")        # 5^2 = 25
print(f"  power(5, 3)  = {power(5, 3)}")     # 5^3 = 125
print(f"  power(2, 10) = {power(2, 10)}")    # 2^10 = 1024


def create_profile(name, age, city="Portland", state="OR"):
    """Create a user profile with optional location defaults."""
    return f"{name}, age {age}, {city}, {state}"

print(f"\n  {create_profile('Preston', 25)}")
print(f"  {create_profile('Alice', 30, 'Seattle', 'WA')}")


# ── Section 4: *args and **kwargs ────────────────────────────

def sum_all(*args):
    """Accept any number of positional arguments and sum them.
    *args collects extra positional arguments into a tuple."""
    total = 0
    for num in args:
        total += num
    return total

print("\n--- *args (Variable Positional Arguments) ---")
print(f"  sum_all(1, 2, 3)        = {sum_all(1, 2, 3)}")
print(f"  sum_all(10, 20, 30, 40) = {sum_all(10, 20, 30, 40)}")


def build_report(**kwargs):
    """Accept any number of keyword arguments and format them.
    **kwargs collects extra keyword arguments into a dictionary."""
    lines = []
    for key, value in kwargs.items():
        lines.append(f"  {key}: {value}")
    return "\n".join(lines)

print("\n--- **kwargs (Variable Keyword Arguments) ---")
print(build_report(name="Preston", course="CIS 133", grade="A", gpa=3.9))


# ── Section 5: Lambda (Anonymous) Functions ─────────────────

# Lambda: small, one-expression functions defined inline
# Syntax: lambda parameters: expression

print("\n--- Lambda Functions ---")
square = lambda x: x ** 2
print(f"  square(9) = {square(9)}")

add = lambda a, b: a + b
print(f"  add(15, 27) = {add(15, 27)}")

# Lambda with sorting
students = [("Preston", 95), ("Alice", 88), ("Bob", 72), ("Carol", 91)]
students_sorted = sorted(students, key=lambda s: s[1], reverse=True)
print("\n  Students sorted by grade (descending):")
for name, grade in students_sorted:
    print(f"    {name}: {grade}")

# Lambda with map() and filter()
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
doubled = list(map(lambda x: x * 2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"\n  Original:  {numbers}")
print(f"  Doubled:   {doubled}")
print(f"  Evens:     {evens}")


# ── Section 6: Recursion ────────────────────────────────────

def factorial(n):
    """Calculate n! recursively.
    Base case: 0! = 1
    Recursive case: n! = n * (n-1)!"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print("\n--- Recursion: Factorial ---")
for i in range(0, 11):
    print(f"  {i}! = {factorial(i)}")


def fibonacci(n):
    """Return the nth Fibonacci number recursively.
    Base cases: fib(0) = 0, fib(1) = 1
    Recursive case: fib(n) = fib(n-1) + fib(n-2)"""
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

print("\n--- Recursion: Fibonacci ---")
fib_nums = [fibonacci(i) for i in range(12)]
print(f"  First 12: {fib_nums}")


def binary_search_recursive(arr, target, low, high):
    """Binary search implemented recursively."""
    if low > high:
        return -1
    mid = (low + high) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, high)
    else:
        return binary_search_recursive(arr, target, low, mid - 1)

print("\n--- Recursion: Binary Search ---")
sorted_data = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
target = 23
result = binary_search_recursive(sorted_data, target, 0, len(sorted_data) - 1)
print(f"  List: {sorted_data}")
print(f"  Search for {target}: found at index {result}")


# ── Section 7: Scope (Local, Global, Nonlocal) ──────────────

global_var = "I am global"

def scope_demo():
    """Demonstrate variable scope rules."""
    local_var = "I am local"
    print(f"  Inside function: {local_var}")
    print(f"  Accessing global: {global_var}")

print("\n--- Variable Scope ---")
scope_demo()
print(f"  Outside function: {global_var}")
# print(local_var)  ← This would cause NameError


# ── Section 8: Type Hints ───────────────────────────────────

def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate Body Mass Index with type-annotated parameters."""
    return round(weight_kg / (height_m ** 2), 1)

def classify_bmi(bmi: float) -> str:
    """Classify a BMI value into a health category."""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25.0:
        return "Normal weight"
    elif bmi < 30.0:
        return "Overweight"
    else:
        return "Obese"

print("\n--- Type Hints ---")
bmi = calculate_bmi(75.0, 1.80)
category = classify_bmi(bmi)
print(f"  BMI: {bmi} → {category}")


# ── Section 9: Decorators ───────────────────────────────────

import time

def timer(func):
    """Decorator that measures and prints function execution time."""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"  {func.__name__} ran in {elapsed:.6f} seconds")
        return result
    return wrapper

@timer
def slow_sum(n):
    """Sum numbers from 1 to n (deliberately using a loop)."""
    total = 0
    for i in range(1, n + 1):
        total += i
    return total

print("\n--- Decorator: Timer ---")
result = slow_sum(1_000_000)
print(f"  Sum of 1 to 1,000,000 = {result:,}")


# ── Section 10: Practical Application ────────────────────────

def grade_calculator(scores: list) -> dict:
    """Calculate comprehensive grade statistics from a list of scores.
    Demonstrates combining multiple function concepts."""
    if not scores:
        return {"error": "No scores provided"}

    total = sum(scores)
    count = len(scores)
    average = total / count
    highest = max(scores)
    lowest = min(scores)

    # Letter grade based on average
    if average >= 90:
        letter = "A"
    elif average >= 80:
        letter = "B"
    elif average >= 70:
        letter = "C"
    elif average >= 60:
        letter = "D"
    else:
        letter = "F"

    return {
        "scores": scores,
        "count": count,
        "total": total,
        "average": round(average, 2),
        "highest": highest,
        "lowest": lowest,
        "range": highest - lowest,
        "letter_grade": letter
    }

print("\n--- Practical: Grade Calculator ---")
my_scores = [95, 87, 92, 78, 88, 91, 85, 96, 73, 90]
report = grade_calculator(my_scores)
for key, value in report.items():
    print(f"  {key:<14} {value}")
