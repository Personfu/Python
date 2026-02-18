# ============================================================
# Assignment — Database Concepts
# CIS 156 — Computer Science Concepts | FLLC Enterprise
# Author: Preston Furulie
# ============================================================
# CompTIA ITF+ Alignment: Software Development domain —
# understanding how data is structured, stored, and queried
# in relational database systems.
# ============================================================

"""
Database Concepts
=================
A database is an organized collection of structured data. Relational
databases use tables with rows and columns, enforcing relationships
through keys. SQL (Structured Query Language) is the standard
language for managing relational data.
"""

import sqlite3
import os


# ────────────────────────────────────────────────────────────
# 1. RELATIONAL DATABASE CONCEPTS
# ────────────────────────────────────────────────────────────

def relational_concepts():
    """Explain core relational database terminology."""
    print(f"\n{'='*60}")
    print("1. RELATIONAL DATABASE CONCEPTS")
    print(f"{'='*60}")

    terms = {
        "Table (Relation)":
            "A structured set of data organized in rows and columns.",
        "Row (Record/Tuple)":
            "A single entry in a table representing one entity.",
        "Column (Field/Attribute)":
            "A named property that every row in the table has.",
        "Primary Key (PK)":
            "A unique identifier for each row — no duplicates, no NULLs.",
        "Foreign Key (FK)":
            "A column referencing a primary key in another table,\n"
            "                    establishing a relationship between tables.",
        "Schema":
            "The blueprint defining tables, columns, types, and constraints.",
        "Index":
            "A data structure that speeds up lookups on a column.",
        "Normalization":
            "Organizing tables to reduce redundancy and dependency.",
    }

    for term, definition in terms.items():
        print(f"\n  {term}")
        print(f"    {definition}")


# ────────────────────────────────────────────────────────────
# 2. DATA TYPES
# ────────────────────────────────────────────────────────────

def data_types_demo():
    """Show common SQL data types and their SQLite equivalents."""
    print(f"\n{'='*60}")
    print("2. COMMON SQL DATA TYPES")
    print(f"{'='*60}")

    types = [
        ("INTEGER",  "Whole numbers",             "employee_id, quantity"),
        ("REAL",     "Floating-point numbers",    "price, temperature"),
        ("TEXT",     "Variable-length strings",   "name, email, address"),
        ("BLOB",     "Binary large object",       "images, files"),
        ("BOOLEAN",  "True/False (0 or 1)",       "is_active, is_admin"),
        ("DATE",     "Calendar date (YYYY-MM-DD)","hire_date, birth_date"),
        ("DATETIME", "Date + time",               "created_at, updated_at"),
    ]

    print(f"\n  {'Type':<12} {'Description':<28} {'Example Columns'}")
    print(f"  {'-'*12} {'-'*28} {'-'*26}")
    for dtype, desc, examples in types:
        print(f"  {dtype:<12} {desc:<28} {examples}")

    print("\n  SQLite uses dynamic typing with 5 storage classes:")
    print("    NULL, INTEGER, REAL, TEXT, BLOB")


# ────────────────────────────────────────────────────────────
# 3. SQL OPERATIONS WITH SQLite
# ────────────────────────────────────────────────────────────
# SQLite is a file-based relational database engine bundled
# with Python's standard library — no server needed.

DB_PATH = ":memory:"  # in-memory database for demonstration


def get_connection():
    """Create an in-memory SQLite database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables(conn):
    """Define the schema: departments and employees."""
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            dept_id   INTEGER PRIMARY KEY,
            name      TEXT NOT NULL UNIQUE,
            location  TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            emp_id     INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name  TEXT NOT NULL,
            email      TEXT NOT NULL UNIQUE,
            dept_id    INTEGER,
            salary     REAL NOT NULL,
            hire_date  TEXT NOT NULL,
            FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
        )
    """)

    conn.commit()
    return cursor


def sql_create_demo(conn):
    """Demonstrate CREATE TABLE and describe the schema."""
    print(f"\n{'='*60}")
    print("3. SQL — CREATE TABLE")
    print(f"{'='*60}")

    cursor = create_tables(conn)

    print("\n  Created tables: departments, employees")
    print("\n  departments:")
    print("    dept_id   INTEGER  PRIMARY KEY")
    print("    name      TEXT     NOT NULL UNIQUE")
    print("    location  TEXT     NOT NULL")

    print("\n  employees:")
    print("    emp_id     INTEGER  PRIMARY KEY")
    print("    first_name TEXT     NOT NULL")
    print("    last_name  TEXT     NOT NULL")
    print("    email      TEXT     NOT NULL UNIQUE")
    print("    dept_id    INTEGER  FOREIGN KEY -> departments(dept_id)")
    print("    salary     REAL     NOT NULL")
    print("    hire_date  TEXT     NOT NULL")


# ────────────────────────────────────────────────────────────
# 4. INSERT — Adding data
# ────────────────────────────────────────────────────────────

def sql_insert_demo(conn):
    """Demonstrate INSERT INTO with parameterized queries."""
    print(f"\n{'='*60}")
    print("4. SQL — INSERT INTO")
    print(f"{'='*60}")

    cursor = conn.cursor()

    departments = [
        (1, "Engineering",  "Building A"),
        (2, "Operations",   "Building B"),
        (3, "Security",     "Building C"),
        (4, "Data Services","Building A"),
    ]
    cursor.executemany(
        "INSERT INTO departments (dept_id, name, location) VALUES (?, ?, ?)",
        departments,
    )

    employees = [
        (101, "Preston",  "Furulie",   "pfurulie@fllc.com",   1, 95000.00, "2024-01-15"),
        (102, "Alice",    "Chen",      "achen@fllc.com",      1, 88000.00, "2024-03-01"),
        (103, "Bob",      "Martinez",  "bmartinez@fllc.com",  2, 72000.00, "2024-06-10"),
        (104, "Carol",    "Johnson",   "cjohnson@fllc.com",   3, 91000.00, "2025-01-05"),
        (105, "David",    "Kim",       "dkim@fllc.com",       4, 85000.00, "2025-02-20"),
        (106, "Eve",      "Patel",     "epatel@fllc.com",     1, 78000.00, "2025-04-15"),
        (107, "Frank",    "Robinson",  "frobinson@fllc.com",  2, 69000.00, "2025-07-01"),
        (108, "Grace",    "Lee",       "glee@fllc.com",       3, 93000.00, "2025-09-10"),
    ]
    cursor.executemany(
        "INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?, ?)",
        employees,
    )
    conn.commit()

    print(f"\n  Inserted {len(departments)} departments and {len(employees)} employees.")
    print("  Used parameterized queries (?) to prevent SQL injection.")


# ────────────────────────────────────────────────────────────
# 5. SELECT — Querying data
# ────────────────────────────────────────────────────────────

def print_results(cursor, title):
    """Helper: print query results as a formatted table."""
    cols = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    widths = [max(len(str(c)), max((len(str(r[i])) for r in rows), default=0))
              for i, c in enumerate(cols)]

    header = "  " + "  ".join(c.ljust(w) for c, w in zip(cols, widths))
    sep = "  " + "  ".join("-" * w for w in widths)
    print(f"\n  {title}")
    print(header)
    print(sep)
    for row in rows:
        line = "  " + "  ".join(str(v).ljust(w) for v, w in zip(row, widths))
        print(line)


def sql_select_demo(conn):
    """Demonstrate SELECT with WHERE, ORDER BY."""
    print(f"\n{'='*60}")
    print("5. SQL — SELECT Queries")
    print(f"{'='*60}")

    cursor = conn.cursor()

    # All employees
    cursor.execute("SELECT emp_id, first_name, last_name, salary FROM employees")
    print_results(cursor, "All Employees:")

    # WHERE clause
    cursor.execute(
        "SELECT first_name, last_name, salary FROM employees WHERE salary > 85000"
    )
    print_results(cursor, "Employees with salary > $85,000:")

    # ORDER BY
    cursor.execute(
        "SELECT first_name, last_name, salary FROM employees ORDER BY salary DESC"
    )
    print_results(cursor, "Employees sorted by salary (descending):")

    # COUNT / aggregate
    cursor.execute("SELECT COUNT(*) AS total, AVG(salary) AS avg_salary FROM employees")
    print_results(cursor, "Aggregate — Count & Average Salary:")


# ────────────────────────────────────────────────────────────
# 6. JOIN — Combining tables
# ────────────────────────────────────────────────────────────

def sql_join_demo(conn):
    """Demonstrate INNER JOIN between employees and departments."""
    print(f"\n{'='*60}")
    print("6. SQL — JOIN (Combining Tables)")
    print(f"{'='*60}")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT e.first_name, e.last_name, d.name AS department, d.location
        FROM employees e
        INNER JOIN departments d ON e.dept_id = d.dept_id
        ORDER BY d.name, e.last_name
    """)
    print_results(cursor, "Employees with Department Info (INNER JOIN):")

    cursor.execute("""
        SELECT d.name AS department, COUNT(e.emp_id) AS headcount,
               ROUND(AVG(e.salary), 2) AS avg_salary
        FROM departments d
        LEFT JOIN employees e ON d.dept_id = e.dept_id
        GROUP BY d.dept_id
        ORDER BY headcount DESC
    """)
    print_results(cursor, "Department Summary (GROUP BY):")

    print("\n  JOIN Types:")
    print("    INNER JOIN — Only matching rows from both tables")
    print("    LEFT JOIN  — All rows from left table + matches from right")
    print("    RIGHT JOIN — All rows from right table + matches from left")
    print("    FULL JOIN  — All rows from both tables")


# ────────────────────────────────────────────────────────────
# 7. UPDATE and DELETE — Modifying data
# ────────────────────────────────────────────────────────────

def sql_update_delete_demo(conn):
    """Demonstrate UPDATE and DELETE operations (CRUD completion)."""
    print(f"\n{'='*60}")
    print("7. SQL — UPDATE and DELETE (CRUD)")
    print(f"{'='*60}")

    cursor = conn.cursor()

    # UPDATE
    print("\n  Giving Preston a 10% raise...")
    cursor.execute(
        "UPDATE employees SET salary = salary * 1.10 WHERE emp_id = 101"
    )
    conn.commit()
    cursor.execute(
        "SELECT first_name, last_name, salary FROM employees WHERE emp_id = 101"
    )
    print_results(cursor, "After UPDATE:")

    # DELETE
    print("\n  Removing the intern record (emp_id 107)...")
    cursor.execute("DELETE FROM employees WHERE emp_id = 107")
    conn.commit()
    cursor.execute("SELECT emp_id, first_name, last_name FROM employees")
    print_results(cursor, "After DELETE:")

    print("\n  CRUD Summary:")
    print("    C — CREATE (INSERT INTO)")
    print("    R — READ   (SELECT)")
    print("    U — UPDATE (UPDATE ... SET)")
    print("    D — DELETE (DELETE FROM)")

    print("\n  Safety tip: ALWAYS use WHERE with UPDATE/DELETE.")
    print("  Without WHERE, the operation affects EVERY row in the table.")


# ────────────────────────────────────────────────────────────
# 8. RELATIONSHIPS AND KEYS
# ────────────────────────────────────────────────────────────

def relationships_demo():
    """Explain relationship types in relational databases."""
    print(f"\n{'='*60}")
    print("8. DATABASE RELATIONSHIPS")
    print(f"{'='*60}")

    relationships = [
        ("One-to-One",
         "Each row in Table A matches exactly one row in Table B.",
         "employee <-> employee_badge"),
        ("One-to-Many",
         "One row in Table A maps to many rows in Table B.",
         "department -> employees"),
        ("Many-to-Many",
         "Rows in A map to many in B and vice versa,\n"
         "                   implemented via a junction table.",
         "students <-> courses (through enrollment table)"),
    ]

    for rel_type, description, example in relationships:
        print(f"\n  {rel_type}")
        print(f"    Definition : {description}")
        print(f"    Example    : {example}")

    print("\n  Key Types:")
    print("    Primary Key (PK)  — Uniquely identifies each row")
    print("    Foreign Key (FK)  — References a PK in another table")
    print("    Composite Key     — PK made of two or more columns")
    print("    Candidate Key     — Column(s) that could serve as PK")


# ────────────────────────────────────────────────────────────
# MAIN — Run all demonstrations
# ────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  CIS 156 — Database Concepts")
    print("  FLLC Enterprise | Preston Furulie | Spring 2026")
    print("=" * 60)

    relational_concepts()
    data_types_demo()

    conn = get_connection()
    try:
        sql_create_demo(conn)
        sql_insert_demo(conn)
        sql_select_demo(conn)
        sql_join_demo(conn)
        sql_update_delete_demo(conn)
    finally:
        conn.close()

    relationships_demo()

    print(f"\n{'='*60}")
    print("  End of Database Concepts Module")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
