# FLLC Engineering Standards
**Author:** Preston Furulie | **Effective:** February 2026

---

## 1. General Principles

1. **Readability over cleverness** — code is read 10x more than it is written
2. **Explicit over implicit** — name things clearly, avoid magic numbers
3. **DRY (Don't Repeat Yourself)** — extract shared logic into functions/modules
4. **YAGNI (You Aren't Gonna Need It)** — don't build features speculatively
5. **Single Responsibility** — each function/class does one thing well
6. **Fail fast** — validate inputs early, throw descriptive errors

---

## 2. Python Standards

### Style
- Follow **PEP 8** (enforced by linter)
- Maximum line length: **100 characters**
- Use **4 spaces** for indentation (never tabs)
- Use **snake_case** for functions and variables
- Use **PascalCase** for class names
- Use **UPPER_SNAKE_CASE** for constants

### Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Variable | snake_case | `user_count` |
| Function | snake_case | `calculate_total()` |
| Class | PascalCase | `LinkedList` |
| Constant | UPPER_SNAKE | `MAX_RETRIES = 3` |
| Private | leading underscore | `_internal_method()` |
| Module | snake_case | `file_io.py` |

### Documentation
- Every module has a header comment with course, author, and topic summary
- Every public function has a docstring explaining purpose, parameters, and return value
- Complex algorithms include Big-O complexity in docstring
- Section separators use `# ── Section Name ──` format

### Example

```python
# ============================================================
# Module Name — Brief Description
# CIS XXX — Course | Preston Furulie
# ============================================================

def calculate_discount(price: float, percent: float) -> float:
    """Calculate the discounted price.

    Args:
        price: Original price (must be >= 0)
        percent: Discount percentage (0-100)

    Returns:
        The price after applying the discount.

    Raises:
        ValueError: If price is negative or percent is out of range.
    """
    if price < 0:
        raise ValueError(f"Price must be >= 0, got {price}")
    if not 0 <= percent <= 100:
        raise ValueError(f"Percent must be 0-100, got {percent}")
    return round(price * (1 - percent / 100), 2)
```

---

## 3. SQL Standards

### Formatting
- **Keywords in UPPERCASE:** `SELECT`, `FROM`, `WHERE`, `JOIN`, `ORDER BY`
- **Table/column names in snake_case:** `product_name`, `order_date`
- **Indent JOINs and WHERE clauses** under the main clause
- **One column per line** in SELECT for readability (when > 3 columns)
- **Always alias** tables in JOINs using meaningful short names

### Naming

| Element | Convention | Example |
|---------|-----------|---------|
| Table | plural snake_case | `order_items` |
| Column | singular snake_case | `product_name` |
| Primary Key | `table_id` | `product_id` |
| Foreign Key | referenced `table_id` | `category_id` |
| Index | `idx_table_column` | `idx_products_category` |
| View | `v_description` | `v_product_catalog` |
| Procedure | `sp_action` | `sp_customer_orders` |
| Constraint | `fk_table_reference` | `fk_products_categories` |

### Example

```sql
SELECT p.product_name,
       c.category_name,
       p.list_price,
       ROUND(p.list_price * (1 - p.discount_percent/100), 2) AS sale_price
FROM products p
    JOIN categories c ON p.category_id = c.category_id
WHERE p.is_active = TRUE
  AND p.list_price > 100
ORDER BY c.category_name, p.product_name;
```

---

## 4. JavaScript Standards

- Use **ES2024+** features (const/let, arrow functions, async/await, optional chaining)
- **Never use `var`** — use `const` by default, `let` when reassignment is needed
- Use **camelCase** for variables and functions, **PascalCase** for classes
- JSDoc comments on all public functions
- Prefer **async/await** over `.then()` chains
- Always handle errors in async functions with try/catch

---

## 5. Infrastructure as Code (Terraform)

- All resources tagged with: `Project`, `Environment`, `ManagedBy`, `Owner`
- Use **variables** for all environment-specific values
- Use **remote state** (S3 + DynamoDB locking)
- Security groups: **deny all by default**, explicitly allow required ports
- Never hardcode secrets — use `sensitive = true` variables or Secrets Manager

---

## 6. Git Workflow

### Commit Messages
- Format: `<type>: <description>`
- Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `security`
- Use present tense: "Add feature" not "Added feature"
- Keep first line under 72 characters

### Examples
```
feat: Add Dijkstra's shortest path to graph engine
fix: Correct off-by-one error in binary search
docs: Expand SRS with acceptance criteria matrix
refactor: Extract common DB connection logic into helper
security: Upgrade bcrypt cost factor from 10 to 12
```

### Branch Strategy
- `main` — production-ready code only
- `develop` — integration branch
- `feature/<name>` — new features
- `fix/<name>` — bug fixes

---

## 7. File Organization

```
Repository Root
├── README.md                  # Enterprise overview
├── ARCHITECTURE.md            # Technical architecture
├── docs/                      # Project management documents
│   ├── project-charter.md
│   ├── enterprise-roadmap.md
│   ├── coding-standards.md    # (this document)
│   └── security-policy.md
├── CIS120/                    # Phase 01: IT Foundations
├── CIS133/                    # Phase 02: Software Engineering
├── CIS195/                    # Phase 03: Web Platform
├── CIS233/                    # Phase 04: Data Architecture
├── CIS275/                    # Phase 05: Core Engineering
├── CIS310/                    # Phase 06: Systems Analysis
├── CIS350/                    # Phase 07: Information Security
├── CIS410/                    # Phase 08: Cloud & DevOps
├── CIS425/                    # Phase 09: Enterprise Platform
└── index.html                 # Coursework display portal
```

Each phase directory contains:
- Source code files (`.py`, `.js`, `.sql`, `.tf`, `.yml`)
- Documentation (`.md`)
- `README.md` — phase overview and file index
