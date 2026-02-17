# ============================================================
# Assignment 3 — Strings and Things: Fun With Strings
# CIS 133 — Intro to Programming | FLLC Enterprise
# Author: Preston Furulie
# ============================================================
# Concepts: len(), string slicing, concatenation, join(),
#           lists, string methods, indexing, iteration
# ============================================================

# Define the original word as a string variable
word = "Supercalifragilisticexpialidocious"

print("=" * 60)
print("  STRINGS AND THINGS — Preston Furulie")
print("=" * 60)

# ── Step 1: Count the letters and print the number ───────────
# len() returns the total number of characters in the string
letter_count = len(word)
print(f"\n1. Letter Count")
print(f"   Word: \"{word}\"")
print(f"   Number of letters: {letter_count}")

# ── Step 2: Print only the first 5 letters ───────────────────
# String slicing: word[start:stop] — start is inclusive, stop is exclusive
# word[:5] is shorthand for word[0:5]
first_five = word[:5]
print(f"\n2. First Five Letters")
print(f"   word[:5] = \"{first_five}\"")

# ── Step 3: Concatenate with another string ──────────────────
# The + operator joins two strings together
phrase = " is something quite atrocious"
combined = word + phrase
print(f"\n3. Concatenation")
print(f"   \"{combined}\"")

# ── Step 4: Break into a list, then rejoin ───────────────────
# Split the word into three parts stored as list elements
word_list = ["Supercali", "fragilistic", "expialidocious"]
print(f"\n4. List Split and Rejoin")
print(f"   List: {word_list}")

# "".join() concatenates all list elements with no separator
# This ensures no whitespaces in the result
rejoined_word = "".join(word_list)
print(f"   Rejoined: \"{rejoined_word}\"")
print(f"   Match original: {rejoined_word == word}")

# ── Step 5: Put your name into a list and print it ───────────
name_list = ["Preston", "Furulie"]
print(f"\n5. Name List")
print(f"   {name_list}")

# ── Extended String Concepts ─────────────────────────────────
print(f"\n{'─' * 60}")
print(f"  Extended String Operations")
print(f"{'─' * 60}")

# String methods
print(f"\n  .upper()     → \"{word[:10].upper()}...\"")
print(f"  .lower()     → \"{word[:10].lower()}...\"")
print(f"  .title()     → \"{word[:10].title()}...\"")
print(f"  .swapcase()  → \"{word[:10].swapcase()}...\"")

# Searching within strings
print(f"\n  .find('cal')     → index {word.find('cal')}")
print(f"  .count('i')      → {word.count('i')} occurrences")
print(f"  .startswith('S') → {word.startswith('S')}")
print(f"  .endswith('ous') → {word.endswith('ous')}")

# Advanced slicing
print(f"\n  Slicing Examples:")
print(f"    word[5:9]    = \"{word[5:9]}\"      (characters 5-8)")
print(f"    word[-8:]    = \"{word[-8:]}\"  (last 8 characters)")
print(f"    word[::2]    = \"{word[::2]}\"  (every 2nd character)")
print(f"    word[::-1]   = \"{word[::-1]}\"  (reversed)")

# String formatting methods
full_name = " ".join(name_list)  # Join with space separator
print(f"\n  Formatting:")
print(f"    ' '.join(name_list) = \"{full_name}\"")
print(f"    f-string:  \"Hello, {full_name}!\"")
print(f"    .center(40, '-') = \"{full_name.center(40, '-')}\"")

# String as iterable
print(f"\n  Character Frequency in \"{word[:20]}...\":")
unique_chars = sorted(set(word.lower()))
for char in unique_chars:
    count = word.lower().count(char)
    bar = "█" * count
    print(f"    '{char}': {count:>2} {bar}")

# String validation methods
test_strings = [("Hello123", "mixed"), ("12345", "digits"), ("HELLO", "alpha"), ("  ", "spaces")]
print(f"\n  Validation Methods:")
for s, label in test_strings:
    print(f"    \"{s}\" ({label}): isalpha={s.isalpha()}, isdigit={s.isdigit()}, isalnum={s.isalnum()}")
