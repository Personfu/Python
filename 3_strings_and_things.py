
# Define the original word as a string variable
word = "Supercalifragilisticexpialidocious"

# --- 1. Count the letters and print the number ---
# The len() function returns the total number of characters in the string
letter_count = len(word)
print("Number of letters:", letter_count)

# Blank line for readability
print()

# --- 2. Print only the first 5 letters ---
# String slicing with [:5] extracts characters from index 0 up to (not including) 5
first_five = word[:5]
print("First five letters:", first_five)

# Blank line for readability
print()

# --- 3. Concatenate with another string ---
# Using the + operator to join the original word with a new phrase
phrase = " is something quite atrocious"
combined = word + phrase
print("Concatenated phrase:", combined)

# Blank line for readability
print()

# --- 4. Break into a list of three elements, then concatenate back together ---
# Create a list containing three parts of the original word
word_list = ["Supercali", "fragilistic", "expialidocious"]

# Use "".join() with an empty string separator to concatenate the list
# elements back together with no white spaces
rejoined_word = "".join(word_list)
print("Rejoined word from list:", rejoined_word)

# Blank line for readability
print()

# --- 5. Put your name into a list and print it ---
# Store first and last name as elements in a list
name_list = ["Preston", "Furulie"]
print("Name list:", name_list)
