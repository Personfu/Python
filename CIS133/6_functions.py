# Functions
# CIS 133 — Intro to Programming | Preston Furulie

# Function to calculate area of a rectangle
def rectangle_area(length, width):
    return length * width

# Function to calculate area of a circle
def circle_area(radius):
    pi = 3.14159
    return pi * radius ** 2

# Function with default parameter
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

# Function that returns multiple values
def min_max(numbers):
    return min(numbers), max(numbers)

# Test all functions
print(greet("Preston"))
print(greet("Preston", "Welcome"))
print()
print("Rectangle (5x3):", rectangle_area(5, 3))
print("Circle (r=7):", round(circle_area(7), 2))
print()
data = [34, 12, 89, 3, 56]
lo, hi = min_max(data)
print("Data:", data)
print("Min:", lo, "Max:", hi)
