# Phase 04 — Data Architecture
**Department:** Data Engineering | **Course:** CIS 233 — Database Management | **Status:** Complete

---

## Purpose

Design and implement FLLC's relational data layer — from table creation and constraint enforcement through complex queries, subqueries, and stored procedures. Establishes the normalized schema patterns used in the enterprise platform.

## Deliverables

| File | Description | Key Concepts |
|------|------------|-------------|
| [`exercise1_create_table.sql`](exercise1_create_table.sql) | DDL and constraint design | `CREATE TABLE`, `PRIMARY KEY`, `FOREIGN KEY` (CASCADE), `AUTO_INCREMENT`, `CHECK`, `UNIQUE`, `ENUM`, `DEFAULT`, `DESCRIBE` |
| [`exercise2_select_where.sql`](exercise2_select_where.sql) | Query patterns (12 sections) | `WHERE` (=, <>, >, BETWEEN, IN, LIKE, IS NULL), compound conditions (AND/OR/NOT), aliases, calculated columns, `DISTINCT`, `LIMIT/OFFSET`, string functions |
| [`exercise3_aggregates.sql`](exercise3_aggregates.sql) | Aggregate functions and grouping | `COUNT/SUM/AVG/MIN/MAX`, `GROUP BY`, `HAVING`, `ROLLUP`, conditional aggregation (`CASE`), date functions (`YEAR/MONTH/DATEDIFF`) |
| [`exercise4_joins_unions.sql`](exercise4_joins_unions.sql) | Multi-table queries | `INNER JOIN`, `LEFT OUTER JOIN`, self-join, `UNION`, table aliases, 4-table joins, filtered joins |
| [`exercise5_dml.sql`](exercise5_dml.sql) | Data manipulation | `INSERT` (auto-ID), `UPDATE`, `DELETE`, foreign key constraints, safe-update mode |
| [`exercise6_subqueries.sql`](exercise6_subqueries.sql) | Advanced query patterns | Scalar subqueries, `IN/ANY/ALL`, correlated subqueries, `EXISTS/NOT EXISTS`, derived tables, CTEs (single and multi-CTE) |
| [`exercise7_views_procedures.sql`](exercise7_views_procedures.sql) | Database objects | `CREATE VIEW` (3 views), `CREATE PROCEDURE` (5 procedures), `IN/OUT` parameters, `IF/ELSE`, error handling (`DECLARE HANDLER`), search procedure |
| [`db_design_er_diagram.md`](db_design_er_diagram.md) | Schema design document | Entity-Relationship diagram (ASCII), relationship summary table, 3NF normalization analysis, intentional denormalization, indexing strategy, data dictionary |

## Database: `my_guitar_shop`

All exercises target the `my_guitar_shop` database with tables: `categories`, `products`, `customers`, `addresses`, `orders`, `order_items`.

## Enterprise Application

- **Phase 09** production schema is built directly on patterns from these exercises
- Views and procedures from exercise 7 inform the API data access layer
- ER diagram methodology applies to all future FLLC database designs
