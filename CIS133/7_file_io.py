# File I/O
# CIS 133 — Intro to Programming | Preston Furulie

# Write employee data to a file
employees = [
    "John Smith, Manager, 75000",
    "Jane Doe, Developer, 85000",
    "Bob Wilson, Analyst, 65000"
]

with open("employees.txt", "w") as file:
    for emp in employees:
        file.write(emp + "\n")
print("Data written to employees.txt")

# Read the file back and display formatted output
print()
print("Employee Report:")
print("-" * 40)

with open("employees.txt", "r") as file:
    for line in file:
        parts = line.strip().split(", ")
        name, title, salary = parts
        print(f"{name:<20} {title:<12} ${salary}")

# Append a new employee
with open("employees.txt", "a") as file:
    file.write("Alice Brown, Designer, 70000\n")
print("\nNew employee appended.")
