# Phase 12 — Advanced SQL & Data Analytics
**Department:** Data Engineering | **Course:** CIS 276DA — Advanced SQL & Data Analytics | **Status:** In Progress

---

## Purpose

Extend FLLC Enterprise's data platform with advanced SQL techniques — stored procedures with complex logic, transaction management, role-based security, triggers for automated business rules, and analytical queries. Bridges the gap between foundational SQL (CIS 233) and production-grade data engineering pipelines.

## Deliverables

| File | Description | Key Concepts |
|------|------------|-------------|
| [`advanced_queries.sql`](advanced_queries.sql) | Complex analytical SQL patterns | Multi-table JOINs (3+), correlated subqueries, `EXISTS`/`NOT EXISTS`, `CASE` expressions, window functions (`ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG`, `LEAD`, `NTILE`), recursive CTEs, pivot/unpivot |
| [`transactions_concurrency.sql`](transactions_concurrency.sql) | Transaction processing & concurrency | `BEGIN`/`COMMIT`/`ROLLBACK`, `SAVEPOINT`, isolation levels (`READ UNCOMMITTED` → `SERIALIZABLE`), locking (shared/exclusive), deadlocks, dirty reads, phantom reads |
| [`security_privileges.sql`](security_privileges.sql) | Database security & access control | `CREATE USER`, `GRANT`/`REVOKE`, role-based access, views for column/row-level security, SQL injection prevention, password management |
| [`triggers_events.sql`](triggers_events.sql) | Triggers, audit trails & event scheduling | `BEFORE`/`AFTER` triggers (INSERT, UPDATE, DELETE), `OLD`/`NEW` references, audit logging, validation triggers, cascading logic, event schedulers |
| [`data_analytics.py`](data_analytics.py) | Python data analytics pipeline | Data cleaning, statistical analysis (mean/median/mode/stdev), ASCII visualization, ETL simulation, aggregation, trend analysis, moving averages, CSV processing |
| [`CIS276DA_complete.txt`](CIS276DA_complete.txt) | Course completion summary | Full phase summary in FLLC enterprise format |

## Database: `my_guitar_shop`

All SQL exercises target the `my_guitar_shop` database with tables: `categories`, `products`, `customers`, `addresses`, `orders`, `order_items`, plus audit/logging tables created by triggers.

## Enterprise Application

- **Phase 04** (CIS 233) foundations are extended with advanced query patterns used here
- Transaction and security patterns apply directly to the FLLC API data access layer
- Trigger-based audit trails satisfy compliance requirements for the enterprise platform
- Data analytics pipeline feeds into Phase 09 reporting and decision support dashboards
