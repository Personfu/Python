# FLLC Developer Onboarding Guide
**Author:** Preston Furulie | **Last Updated:** February 2026

---

## Welcome to the FLLC Engineering Team

This guide will get you set up to work on the FLLC Enterprise IT Infrastructure project. After following these steps, you'll be able to run every component locally.

---

## 1. Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.10+ | Software engineering modules (Phases 02, 05, 07, 09) |
| Node.js | 20 LTS | API server and build tools (Phases 03, 09) |
| MySQL | 8.0 | Relational database (Phases 04, 09) |
| Docker | 24+ | Container builds and local stack (Phase 08) |
| Git | 2.40+ | Version control |
| Terraform | 1.5+ | Infrastructure as Code (Phase 08, optional) |
| AWS CLI | 2.x | Cloud operations (Phase 08, optional) |

### Quick Install (Windows)

```powershell
# Python
winget install Python.Python.3.12

# Node.js
winget install OpenJS.NodeJS.LTS

# MySQL
winget install Oracle.MySQL

# Docker Desktop
winget install Docker.DockerDesktop

# Git (likely already installed)
winget install Git.Git
```

### Quick Install (macOS)

```bash
brew install python@3.12 node@20 mysql docker git terraform awscli
```

---

## 2. Repository Setup

```bash
# Clone the repository
git clone https://github.com/Personfu/Python.git
cd Python

# Verify Python
python --version  # Should show 3.10+
```

---

## 3. Running Components

### Phase 02 — Python Modules

```bash
# Run any module directly
python CIS133/1_hello_world_basic_math.py
python CIS133/5_loops_and_iteration.py
python CIS133/8_classes_oop.py
```

### Phase 04 — MySQL Exercises

```bash
# Start MySQL and load the guitar shop database
mysql -u root -p

# Inside MySQL:
SOURCE CIS425/schema.sql;

# Run any exercise
SOURCE CIS233/exercise4_joins_unions.sql;
```

### Phase 05 — Algorithm Library

```bash
# Sorting benchmarks
python CIS275/sorting_algorithms.py

# Graph traversal demos
python CIS275/graph_traversal.py

# BST interactive demo
python CIS275/binary_search_tree.py
```

### Phase 07 — Security Toolkit

```bash
# Encryption and hashing demos
python CIS350/encryption_hashing.py
```

### Phase 08 — Docker Local Stack

```bash
cd CIS410

# Start the full development environment (5 services)
docker compose up -d

# Services:
#   API:     http://localhost:3000
#   MySQL:   localhost:3306
#   Redis:   localhost:6379
#   Nginx:   http://localhost:80
#   Adminer: http://localhost:8081 (DB GUI)

# Verify health
docker compose ps

# Stop
docker compose down
```

### Phase 09 — REST API Server

```bash
# Start the Python API server
python CIS425/api_server.py

# Available at: http://localhost:8080
# Try: http://localhost:8080/api/products
# Try: http://localhost:8080/api/health
```

### Coursework Portal

```
# Open in your browser
index.html
```

---

## 4. Project Structure

```
Python/
├── README.md               ← Start here
├── ARCHITECTURE.md          ← Enterprise architecture
├── CHANGELOG.md             ← Version history
├── docs/                    ← Project management
│   ├── project-charter.md
│   ├── enterprise-roadmap.md
│   ├── coding-standards.md  ← Read before writing code
│   ├── security-policy.md
│   └── onboarding-guide.md  ← You are here
├── CIS120/                  ← Phase 01: IT Foundations
├── CIS133/                  ← Phase 02: Software Engineering
├── CIS195/                  ← Phase 03: Web Platform
├── CIS233/                  ← Phase 04: Data Architecture
├── CIS275/                  ← Phase 05: Core Engineering
├── CIS310/                  ← Phase 06: Systems Analysis
├── CIS350/                  ← Phase 07: InfoSec
├── CIS410/                  ← Phase 08: Cloud & DevOps
├── CIS425/                  ← Phase 09: Enterprise Platform
└── index.html               ← Coursework portal
```

---

## 5. Coding Standards Summary

Before writing any code, read [`docs/coding-standards.md`](coding-standards.md) in full. Key rules:

| Language | Style | Example |
|----------|-------|---------|
| Python | PEP 8, snake_case, docstrings | `def calculate_total(items):` |
| SQL | UPPERCASE keywords, snake_case tables | `SELECT p.product_name FROM products p` |
| JavaScript | camelCase, const by default, async/await | `const fetchData = async () => {}` |
| Terraform | snake_case resources, tagged resources | `resource "aws_vpc" "main" {}` |
| Git | `type: description` commits | `feat: Add graph traversal engine` |

---

## 6. Key Contacts

| Role | Name | Responsibility |
|------|------|---------------|
| Project Lead | Preston Furulie | Architecture, development, delivery |
| Organization | FLLC | Find You Person |
| Academic | PCC CIS Department | Course compliance |

---

## 7. Reference Documents

| Document | Description |
|----------|------------|
| [`README.md`](../README.md) | Enterprise overview with phase map |
| [`ARCHITECTURE.md`](../ARCHITECTURE.md) | Full infrastructure design |
| [`docs/project-charter.md`](project-charter.md) | Scope, risks, timeline |
| [`docs/enterprise-roadmap.md`](enterprise-roadmap.md) | Phase timeline |
| [`docs/security-policy.md`](security-policy.md) | Security requirements |
