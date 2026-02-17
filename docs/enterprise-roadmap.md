# FLLC Enterprise IT — Roadmap
**Author:** Preston Furulie | **Version:** 2.0

---

## Phase Timeline

```
2025 Q1  │  Q2  │  Q3  │  Q4  │  2026 Q1  │  Q2
─────────┼──────┼──────┼──────┼───────────┼──────
█████████│      │      │      │           │        Phase 01: IT Foundations
         │██████│      │      │           │        Phase 02: Software Engineering
         │      │██████│      │           │        Phase 03: Web Platform
         │      │██████│      │           │        Phase 04: Data Architecture
         │      │      │██████│           │        Phase 05: Core Engineering
         │      │      │██████│           │        Phase 06: Systems Analysis
         │      │      │      │███████████│        Phase 07: InfoSec
         │      │      │      │███████████│        Phase 08: Cloud & DevOps
         │      │      │      │           │██████  Phase 09: Enterprise Platform
```

---

## Phase Details

### Phase 01 — IT Foundations
**Timeline:** Q1 2025 | **Status:** Complete | **Course:** CIS 120

| Deliverable | File | Lines |
|------------|------|-------|
| Binary & Number Systems converter | `CIS120/binary_number_systems.py` | 200+ |
| Hardware & Software Fundamentals | `CIS120/hardware_software_fundamentals.md` | 140+ |
| Introduction to Algorithms | `CIS120/intro_to_algorithms.md` | 220+ |

**Milestone:** Team has foundational understanding of computing architecture, data representation, and algorithmic thinking.

---

### Phase 02 — Software Engineering
**Timeline:** Q2 2025 | **Status:** Complete | **Course:** CIS 133

| Deliverable | File | Concepts |
|------------|------|----------|
| Hello World & Basic Math | `CIS133/1_hello_world_basic_math.py` | I/O, arithmetic, formatting |
| Variables & Types | `CIS133/2_variables_and_types.py` | Float, conversion formulas |
| Strings & Things | `CIS133/3_strings_and_things.py` | Slicing, concatenation, lists |
| Movie Age Check | `CIS133/4_movie_age_check.py` | Branching logic (if/elif/else) |
| Loops & Iteration | `CIS133/5_loops_and_iteration.py` | For, while, break, comprehensions, patterns |
| Functions | `CIS133/6_functions.py` | Args, kwargs, lambda, recursion, decorators |
| File I/O | `CIS133/7_file_io.py` | Text, CSV, JSON, error handling, os.path |
| Classes & OOP | `CIS133/8_classes_oop.py` | Inheritance, polymorphism, abstract classes |

**Milestone:** Full Python engineering capability established — from basic I/O to production-grade OOP.

---

### Phase 03 — Web Platform Engineering
**Timeline:** Q3 2025 | **Status:** Complete | **Course:** CIS 195

| Deliverable | File | Concepts |
|------------|------|----------|
| Portfolio SPA | `CIS195/portfolio.html` | Semantic HTML5, CSS custom properties, flexbox, grid |
| DOM Manipulation Framework | `CIS195/dom_manipulation.js` | Event delegation, localStorage, TaskManager app |
| Responsive Design System | `CIS195/responsive_design.css` | Mobile-first, 4 breakpoints, dark/light theme, print |
| REST API Client | `CIS195/rest_api.js` | Fetch, async/await, retry, AbortController, APIClient class |

**Milestone:** Frontend engineering capability with responsive, accessible, API-integrated web applications.

---

### Phase 04 — Data Architecture
**Timeline:** Q3 2025 | **Status:** Complete | **Course:** CIS 233

| Deliverable | File | Concepts |
|------------|------|----------|
| CREATE TABLE & Constraints | `CIS233/exercise1_create_table.sql` | PK, FK, CHECK, UNIQUE, ENUM, CASCADE |
| SELECT & WHERE | `CIS233/exercise2_select_where.sql` | 12 query patterns, LIKE, BETWEEN, aliases |
| Aggregates & GROUP BY | `CIS233/exercise3_aggregates.sql` | COUNT/SUM/AVG, HAVING, ROLLUP, CASE |
| JOINs & UNION | `CIS233/exercise4_joins_unions.sql` | INNER, LEFT, self-join, UNION, aliases |
| INSERT/UPDATE/DELETE | `CIS233/exercise5_dml.sql` | DML operations, AUTO_INCREMENT, safe mode |
| Subqueries & CTEs | `CIS233/exercise6_subqueries.sql` | Correlated, EXISTS, derived tables, CTEs |
| Views & Procedures | `CIS233/exercise7_views_procedures.sql` | CREATE VIEW, stored procedures, error handling |
| ER Diagram & Design | `CIS233/db_design_er_diagram.md` | 3NF normalization, indexing strategy, data dictionary |

**Milestone:** Complete SQL mastery and normalized database design capability.

---

### Phase 05 — Core Algorithm Library
**Timeline:** Q4 2025 | **Status:** Complete | **Course:** CIS 275

| Deliverable | File | Concepts |
|------------|------|----------|
| Linked List Library | `CIS275/linked_list.py` | Singly + doubly, 15 operations, cycle detection |
| Binary Search Tree | `CIS275/binary_search_tree.py` | Insert, delete (3 cases), 4 traversals, validation |
| Sorting Algorithms | `CIS275/sorting_algorithms.py` | 7 algorithms with benchmarking, complexity table |
| Graph Engine | `CIS275/graph_traversal.py` | BFS, DFS, Dijkstra's, topological sort, cycle detection |

**Milestone:** Reusable algorithm library with verified O(n log n) sorting and O(V+E) graph traversal.

---

### Phase 06 — Systems Analysis & Project Management
**Timeline:** Q4 2025 | **Status:** Complete | **Course:** CIS 310

| Deliverable | File | Concepts |
|------------|------|----------|
| Software Requirements Spec | `CIS310/requirements_document.md` | 40+ requirements, MoSCoW priority, acceptance criteria |
| Use Case Documentation | `CIS310/use_cases.md` | 6 use cases with flows, exceptions, business rules |
| System Architecture Design | `CIS310/system_architecture.md` | Three-tier design, caching strategy, scaling plan |

**Milestone:** Professional requirements engineering and architecture design capability.

---

### Phase 07 — Information Security
**Timeline:** Q1 2026 | **Status:** Complete | **Course:** CIS 350

| Deliverable | File | Concepts |
|------------|------|----------|
| Encryption & Hashing Toolkit | `CIS350/encryption_hashing.py` | SHA/HMAC/PBKDF2, Caesar/XOR cipher, password analyzer |
| Network Topology Design | `CIS350/network_topology.md` | 8 VLANs, equipment specs, wireless, redundancy |
| Vulnerability Assessment | `CIS350/vulnerability_assessment.md` | Nessus scan, 3 critical CVEs, remediation matrix |
| Firewall Configuration | `CIS350/firewall_rules.conf` | 10 Palo Alto zone-based rules, implicit deny |

**Milestone:** Comprehensive security posture with defense-in-depth across all layers.

---

### Phase 08 — Cloud & DevOps
**Timeline:** Q1 2026 | **Status:** Complete | **Course:** CIS 410

| Deliverable | File | Concepts |
|------------|------|----------|
| AWS VPC Infrastructure | `CIS410/vpc_design.tf` | VPC, 9 subnets (3-tier × 3 AZ), NAT, flow logs |
| Production Dockerfile | `CIS410/Dockerfile` | Multi-stage, non-root user, healthcheck, OCI labels |
| Docker Compose Stack | `CIS410/docker-compose.yml` | 5 services, secrets, healthchecks, resource limits |
| CI/CD Pipeline | `CIS410/deploy.yml` | 6-stage GitHub Actions with auto-rollback |
| AWS Services (RDS, ECS, ALB) | `CIS410/infrastructure.tf` | RDS Multi-AZ, ECS Fargate, ALB with TLS |

**Milestone:** Fully automated infrastructure provisioning and deployment pipeline.

---

### Phase 09 — Enterprise Platform (Capstone)
**Timeline:** Q2 2026 | **Status:** Complete | **Course:** CIS 425

| Deliverable | File | Concepts |
|------------|------|----------|
| Project Proposal | `CIS425/capstone_proposal.md` | Problem statement, tech stack, timeline, risk assessment |
| Production Schema | `CIS425/schema.sql` | 10 tables, 3NF, full-text search, views, seed data |
| REST API Server | `CIS425/api_server.py` | 15 endpoints, auth, pagination, filtering, CORS |
| API Documentation | `CIS425/api_documentation.md` | Full endpoint reference with examples |
| Deployment Architecture | `CIS425/deployment_architecture.md` | AWS production deployment, scaling, DR |
| Final Presentation | `CIS425/final_presentation.md` | 14-slide deck with metrics and demo plan |

**Milestone:** Production-ready enterprise platform integrating all prior phases.

---

## Post-Delivery Roadmap (Future)

| Phase | Name | Timeline | Priority |
|-------|------|----------|----------|
| 10 | Mobile Application (React Native) | Q3 2026 | High |
| 11 | Machine Learning Analytics | Q4 2026 | Medium |
| 12 | Multi-Tenant SaaS Conversion | Q1 2027 | Medium |
| 13 | Kubernetes Migration (EKS) | Q2 2027 | Low |
