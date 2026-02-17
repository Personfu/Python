# Binary & Number Systems Converter
# CIS 120 — Intro to Computing | Preston Furulie

def convert_number(decimal_num):
    """Convert a decimal number to binary, octal, and hexadecimal."""
    binary = bin(decimal_num)
    octal = oct(decimal_num)
    hexadecimal = hex(decimal_num)
    return binary, octal, hexadecimal

# Get input from user
number = int(input("Enter a decimal number: "))

binary, octal, hexadecimal = convert_number(number)

print("Decimal:", number)
print("Binary:", binary)
print("Octal:", octal)
print("Hexadecimal:", hexadecimal)
print()

# Reverse: binary string to decimal
binary_input = input("Enter a binary number: ")
decimal_result = int(binary_input, 2)
print("Binary", binary_input, "= Decimal", decimal_result)
