# ============================================================
# File I/O — Complete Implementation
# CIS 133 — Intro to Programming | Preston Furulie
# ============================================================
# Covers: text files (read, write, append), file modes, with
# statement, CSV processing, JSON handling, error handling,
# os.path utilities, binary files, and practical applications.
# ============================================================

import os
import json
import csv

print("=" * 60)
print("  FILE I/O — CIS 133 | Preston Furulie")
print("=" * 60)


# ── Section 1: Writing Text Files ───────────────────────────

# "w" mode: write (creates file, overwrites if exists)
# Always use 'with' to ensure the file is properly closed

employees = [
    {"name": "John Smith",    "title": "Manager",   "salary": 75000},
    {"name": "Jane Doe",      "title": "Developer", "salary": 85000},
    {"name": "Bob Wilson",    "title": "Analyst",   "salary": 65000},
    {"name": "Alice Brown",   "title": "Designer",  "salary": 70000},
    {"name": "Charlie Davis",  "title": "DBA",       "salary": 78000},
]

print("\n--- Writing Text File ---")
with open("employees.txt", "w") as file:
    # Write a header line
    file.write(f"{'Name':<20} {'Title':<12} {'Salary':>10}\n")
    file.write("-" * 44 + "\n")

    for emp in employees:
        line = f"{emp['name']:<20} {emp['title']:<12} ${emp['salary']:>9,}\n"
        file.write(line)

print("  Written 5 employees to employees.txt")


# ── Section 2: Reading Text Files ───────────────────────────

# "r" mode: read (default, file must exist)

print("\n--- Reading Entire File ---")
with open("employees.txt", "r") as file:
    contents = file.read()  # read entire file as one string
    print(contents)

# Reading line by line (memory-efficient for large files)
print("--- Reading Line by Line ---")
with open("employees.txt", "r") as file:
    line_number = 0
    for line in file:
        line_number += 1
        print(f"  Line {line_number}: {line.rstrip()}")

# Reading into a list of lines
print("\n--- readlines() ---")
with open("employees.txt", "r") as file:
    lines = file.readlines()
    print(f"  Total lines in file: {len(lines)}")
    print(f"  First line: {lines[0].strip()}")
    print(f"  Last line:  {lines[-1].strip()}")


# ── Section 3: Appending to Files ───────────────────────────

# "a" mode: append (adds to end, creates if doesn't exist)

print("\n--- Appending to File ---")
new_employees = [
    {"name": "Diana Prince", "title": "Lead Dev",  "salary": 95000},
    {"name": "Eve Torres",   "title": "QA Engineer", "salary": 68000},
]

with open("employees.txt", "a") as file:
    for emp in new_employees:
        line = f"{emp['name']:<20} {emp['title']:<12} ${emp['salary']:>9,}\n"
        file.write(line)
print(f"  Appended {len(new_employees)} employees")


# ── Section 4: CSV File Processing ──────────────────────────

# CSV (Comma-Separated Values) — standard tabular data format

print("\n--- Writing CSV ---")
with open("grades.csv", "w", newline="") as file:
    writer = csv.writer(file)
    # Write header row
    writer.writerow(["Student", "Assignment1", "Assignment2", "Midterm", "Final"])
    # Write data rows
    writer.writerow(["Preston Furulie", 95, 92, 88, 94])
    writer.writerow(["Alice Johnson",   87, 90, 85, 91])
    writer.writerow(["Bob Martinez",    78, 82, 75, 80])
    writer.writerow(["Carol Williams",  92, 88, 91, 95])
    writer.writerow(["Dave Thompson",   65, 70, 68, 72])
print("  Written grades.csv with 5 students")

print("\n--- Reading CSV ---")
with open("grades.csv", "r") as file:
    reader = csv.reader(file)
    header = next(reader)  # skip header row
    print(f"  Columns: {header}")
    print()
    for row in reader:
        name = row[0]
        scores = [int(s) for s in row[1:]]
        average = sum(scores) / len(scores)
        print(f"  {name:<20} Scores: {scores}  Avg: {average:.1f}")

# CSV with DictReader (access columns by name)
print("\n--- CSV DictReader ---")
with open("grades.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        final = int(row["Final"])
        status = "PASS" if final >= 70 else "FAIL"
        print(f"  {row['Student']:<20} Final: {final}  [{status}]")


# ── Section 5: JSON File Processing ─────────────────────────

# JSON (JavaScript Object Notation) — standard data interchange format
# Maps directly to Python dictionaries and lists

print("\n--- Writing JSON ---")
inventory = {
    "store": "Guitar Shop",
    "last_updated": "2026-02-15",
    "categories": [
        {
            "name": "Guitars",
            "products": [
                {"id": 1, "name": "Fender Stratocaster", "price": 1199.99, "stock": 12},
                {"id": 2, "name": "Gibson Les Paul",     "price": 2499.99, "stock": 5},
            ]
        },
        {
            "name": "Keyboards",
            "products": [
                {"id": 3, "name": "Yamaha DGX-670", "price": 799.99, "stock": 8},
            ]
        }
    ]
}

with open("inventory.json", "w") as file:
    json.dump(inventory, file, indent=4)  # indent for readability
print("  Written inventory.json")

print("\n--- Reading JSON ---")
with open("inventory.json", "r") as file:
    data = json.load(file)

print(f"  Store: {data['store']}")
print(f"  Updated: {data['last_updated']}")
for category in data["categories"]:
    print(f"\n  Category: {category['name']}")
    for product in category["products"]:
        print(f"    {product['name']:<25} ${product['price']:>8.2f}  (stock: {product['stock']})")


# ── Section 6: Error Handling with Files ────────────────────

print("\n--- Error Handling ---")

# FileNotFoundError
try:
    with open("nonexistent_file.txt", "r") as file:
        data = file.read()
except FileNotFoundError:
    print("  Caught FileNotFoundError: file does not exist")

# PermissionError
try:
    with open("/root/protected.txt", "w") as file:
        file.write("test")
except PermissionError:
    print("  Caught PermissionError: no write permission")
except OSError as e:
    print(f"  Caught OSError: {e}")

# Generic exception handling for file operations
def safe_read(filepath):
    """Read a file with full error handling. Returns content or None."""
    try:
        with open(filepath, "r") as file:
            return file.read()
    except FileNotFoundError:
        print(f"  Error: '{filepath}' not found")
        return None
    except PermissionError:
        print(f"  Error: No permission to read '{filepath}'")
        return None
    except Exception as e:
        print(f"  Unexpected error: {e}")
        return None

safe_read("missing.txt")


# ── Section 7: os.path Utilities ────────────────────────────

print("\n--- os.path Utilities ---")
test_path = "employees.txt"

print(f"  File exists:    {os.path.exists(test_path)}")
print(f"  Is file:        {os.path.isfile(test_path)}")
print(f"  Is directory:   {os.path.isdir(test_path)}")
print(f"  File size:      {os.path.getsize(test_path)} bytes")
print(f"  Absolute path:  {os.path.abspath(test_path)}")
print(f"  Directory:      {os.path.dirname(os.path.abspath(test_path))}")
print(f"  Filename:       {os.path.basename(test_path)}")
print(f"  Extension:      {os.path.splitext(test_path)[1]}")

# List files in current directory
print("\n--- Files in Current Directory ---")
for item in os.listdir("."):
    if os.path.isfile(item):
        size = os.path.getsize(item)
        print(f"  {item:<35} {size:>8} bytes")


# ── Section 8: Practical Application — Log Analyzer ─────────

print("\n--- Practical: Log File Generator & Analyzer ---")

# Generate a sample log file
log_entries = [
    "2026-02-15 08:00:01 INFO  Server started on port 3000",
    "2026-02-15 08:00:05 INFO  Database connection established",
    "2026-02-15 08:01:12 WARN  High memory usage: 85%",
    "2026-02-15 08:02:30 ERROR Failed to process order #1042",
    "2026-02-15 08:02:31 ERROR Stack trace: NullPointerException",
    "2026-02-15 08:03:45 INFO  Order #1043 processed successfully",
    "2026-02-15 08:05:00 WARN  Slow query detected: 2.3s",
    "2026-02-15 08:06:22 INFO  Cache cleared",
    "2026-02-15 08:07:15 ERROR Connection timeout to payment gateway",
    "2026-02-15 08:08:00 INFO  Retry successful for payment gateway",
]

with open("server.log", "w") as file:
    for entry in log_entries:
        file.write(entry + "\n")

# Analyze the log file
with open("server.log", "r") as file:
    info_count = 0
    warn_count = 0
    error_count = 0
    errors = []

    for line in file:
        line = line.strip()
        if "INFO" in line:
            info_count += 1
        elif "WARN" in line:
            warn_count += 1
        elif "ERROR" in line:
            error_count += 1
            errors.append(line)

print(f"  Log Analysis Results:")
print(f"    INFO entries:  {info_count}")
print(f"    WARN entries:  {warn_count}")
print(f"    ERROR entries: {error_count}")
print(f"    Total entries: {info_count + warn_count + error_count}")
print(f"\n  Error details:")
for err in errors:
    print(f"    {err}")


# ── Cleanup ─────────────────────────────────────────────────

# Clean up generated files
for f in ["employees.txt", "grades.csv", "inventory.json", "server.log"]:
    if os.path.exists(f):
        os.remove(f)
print("\n  Cleaned up temporary files.")
