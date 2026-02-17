
# --- Fahrenheit to Celsius Conversion ---

# Using float() to handle decimal temperature values (proper variable type)
fahrenheit = float(input("Enter temperature in Fahrenheit: "))

# Apply the Fahrenheit-to-Celsius conversion formula: C = (F - 32) * 5/9
celsius = (fahrenheit - 32) * 5 / 9

# Display the converted Celsius temperature
print("Temperature in Celsius:", celsius)

# Blank line for readability between the two conversions
print()

# --- Celsius to Fahrenheit Conversion ---

# Prompt the user to enter a temperature in Celsius
# Again using float() for proper decimal handling
celsius = float(input("Enter temperature in Celsius: "))

# Apply the Celsius-to-Fahrenheit conversion formula: F = (C * 9/5) + 32
fahrenheit = (celsius * 9 / 5) + 32

# Display the converted Fahrenheit temperature
print("Temperature in Fahrenheit:", fahrenheit)
