# Loops & Iteration
# CIS 133 — Intro to Programming | Preston Furulie

# Multiplication table using nested for loops
print("Multiplication Table (1-5):")
print("-" * 30)

for i in range(1, 6):
    for j in range(1, 6):
        print(f"{i * j:4}", end="")
    print()

print()

# While loop: countdown
count = 5
print("Countdown:")
while count > 0:
    print(count)
    count -= 1
print("Liftoff!")

print()

# Sum of even numbers from 1 to 20
total = 0
for num in range(2, 21, 2):
    total += num
print("Sum of even numbers 1-20:", total)
