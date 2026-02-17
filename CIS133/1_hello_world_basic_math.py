
# Prompt the user to enter their name and store it in a variable
name = input("Preston: ")

# Prompt the user to enter their yearly salary and convert the input to a float
# so we can perform arithmetic on it
yearly_salary = float(input("50000: "))

# Calculate the monthly salary by dividing the yearly salary by 12 months
monthly_salary = yearly_salary / 12

# Display the greeting along with the calculated monthly salary,
# formatted to two decimal places for proper currency display
print("Hello", name, "your monthly salary is", format(monthly_salary, ".2f"))
