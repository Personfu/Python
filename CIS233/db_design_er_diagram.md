# Database Design & Entity-Relationship Diagram
## CIS 233 — Database Management | Preston Furulie

---

## 1. Design Requirements

Design a normalized relational database for the Guitar Shop e-commerce system supporting:
- Product catalog with categories and suppliers
- Customer accounts with multiple shipping addresses
- Order processing with line items and payment tracking
- Inventory management with stock movement logging
- Product reviews and ratings

---

## 2. Entity-Relationship Diagram

```
┌──────────────────┐          ┌──────────────────┐
│    suppliers     │          │   categories     │
├──────────────────┤          ├──────────────────┤
│ PK supplier_id   │          │ PK category_id   │
│    company_name  │          │    category_name │
│    contact_name  │          │    description   │
│    contact_email │          │    parent_id (FK)│──┐ self-reference
│    phone         │          │    sort_order    │  │ (subcategories)
│    address       │          │    is_active     │◄─┘
└────────┬─────────┘          └────────┬─────────┘
         │ 1                           │ 1
         │                             │
         │ supplies                    │ categorizes
         │                             │
         │ M                           │ M
┌────────┴─────────────────────────────┴─────────┐
│                   products                       │
├──────────────────────────────────────────────────┤
│ PK product_id                                    │
│ FK category_id      → categories.category_id     │
│ FK supplier_id      → suppliers.supplier_id      │
│    product_code     (UNIQUE)                     │
│    product_name                                  │
│    description      (TEXT)                       │
│    list_price       (DECIMAL 10,2)               │
│    cost_price       (DECIMAL 10,2)               │
│    discount_percent (DECIMAL 5,2)                │
│    quantity_on_hand (INT)                         │
│    reorder_point    (INT)                         │
│    date_added       (DATETIME)                   │
│    is_active        (BOOLEAN)                    │
└──────┬───────────────────┬───────────────────────┘
       │ 1                 │ 1
       │                   │
       │                   │ reviewed by
       │                   │
       │                   │ M
       │          ┌────────┴─────────┐
       │          │     reviews      │
       │          ├──────────────────┤
       │          │ PK review_id     │
       │          │ FK product_id    │──→ products
       │          │ FK customer_id   │──→ customers
       │          │    rating (1-5)  │
       │          │    review_title  │
       │          │    review_text   │
       │          │    review_date   │
       │          │    is_verified   │
       │          └──────────────────┘
       │
       │ ordered in                    ┌──────────────────┐
       │                               │   customers      │
       │ M                             ├──────────────────┤
┌──────┴───────────┐                   │ PK customer_id   │
│   order_items    │                   │    email_address  │ (UNIQUE)
├──────────────────┤                   │    password_hash  │
│ PK item_id       │                   │    first_name     │
│ FK order_id      │──→ orders         │    last_name      │
│ FK product_id    │──→ products       │ FK billing_addr_id│──→ addresses
│    item_price    │                   │ FK shipping_addr_id│──→ addresses
│    discount_amount│                  │    created_at     │
│    quantity      │                   │    is_active      │
└──────────────────┘                   └────────┬─────────┘
                                                │ 1
       ┌──────────────────┐                     │
       │     orders       │                     │ places
       ├──────────────────┤                     │
       │ PK order_id      │                     │ M
       │ FK customer_id   │────────────────────→┘
       │    order_date    │
       │    ship_date     │
       │    ship_amount   │
       │    tax_amount    │
       │    order_status  │ (pending, processing, shipped, delivered, cancelled)
       │    payment_type  │ (credit, debit, paypal)
       │    card_last_four│
       └────────┬─────────┘
                │ 1                    ┌──────────────────┐
                │                      │    addresses     │
                │ has items            ├──────────────────┤
                │                      │ PK address_id    │
                │ M                    │ FK customer_id   │──→ customers
       ┌────────┘                      │    line1         │
       │                               │    line2         │
       └──→ order_items               │    city          │
                                       │    state         │
                                       │    zip_code      │
       ┌──────────────────┐            │    phone         │
       │  inventory_log   │            │    is_default    │
       ├──────────────────┤            │    address_type  │ (billing, shipping)
       │ PK log_id        │            └──────────────────┘
       │ FK product_id    │──→ products
       │    change_type   │ (restock, sale, return, adjustment)
       │    quantity_change│
       │    unit_cost     │
       │    logged_by     │
       │    log_date      │
       │    reference_id  │ (order_id or PO number)
       └──────────────────┘
```

---

## 3. Relationship Summary

| Relationship              | Type      | Cardinality | FK Location    | Referential Action      |
|--------------------------|-----------|-------------|----------------|-------------------------|
| categories → products     | One-to-Many | 1:M       | products.category_id | ON DELETE RESTRICT  |
| suppliers → products      | One-to-Many | 1:M       | products.supplier_id | ON DELETE RESTRICT  |
| categories → categories   | Self-referencing | 1:M  | categories.parent_id | ON DELETE SET NULL  |
| customers → orders        | One-to-Many | 1:M       | orders.customer_id   | ON DELETE RESTRICT  |
| customers → addresses     | One-to-Many | 1:M       | addresses.customer_id| ON DELETE CASCADE   |
| orders → order_items      | One-to-Many | 1:M       | order_items.order_id | ON DELETE CASCADE   |
| products → order_items    | One-to-Many | 1:M       | order_items.product_id| ON DELETE RESTRICT |
| products → reviews        | One-to-Many | 1:M       | reviews.product_id   | ON DELETE CASCADE   |
| customers → reviews       | One-to-Many | 1:M       | reviews.customer_id  | ON DELETE CASCADE   |
| products → inventory_log  | One-to-Many | 1:M       | inventory_log.product_id | ON DELETE CASCADE|

---

## 4. Normalization Analysis

### First Normal Form (1NF)
- All columns contain atomic (indivisible) values
- Each row is uniquely identified by a primary key
- No repeating groups (e.g., address is a separate table, not multiple columns on customers)

### Second Normal Form (2NF)
- Satisfies 1NF
- No partial dependencies: all non-key columns depend on the **entire** primary key
- Example: `order_items` has a composite logical key (order_id, product_id); `item_price` depends on both

### Third Normal Form (3NF)
- Satisfies 2NF
- No transitive dependencies: non-key columns don't depend on other non-key columns
- Example: `category_name` is in `categories` table, not duplicated in `products`
- Exception: `item_price` in `order_items` intentionally denormalized (snapshot of price at time of order)

### Denormalization Decisions (Intentional)

| Column                     | Table        | Reason                                        |
|---------------------------|--------------|-----------------------------------------------|
| item_price                | order_items  | Snapshot: product price may change after order |
| discount_amount           | order_items  | Snapshot: discount may change after order      |
| quantity_on_hand          | products     | Denormalized for read performance; inventory_log is the source of truth |

---

## 5. Indexing Strategy

| Table          | Index                              | Type      | Purpose                        |
|----------------|------------------------------------|-----------|--------------------------------|
| products       | idx_products_category              | B-Tree    | Filter by category (JOINs)     |
| products       | idx_products_name                  | Full-text | Product search                 |
| products       | uq_products_code                   | Unique    | Enforce unique product codes    |
| orders         | idx_orders_customer                | B-Tree    | Customer order lookup           |
| orders         | idx_orders_date                    | B-Tree    | Date range queries              |
| order_items    | idx_oi_order                       | B-Tree    | Join with orders                |
| order_items    | idx_oi_product                     | B-Tree    | Product sales analysis          |
| customers      | uq_customers_email                 | Unique    | Login lookup, prevent duplicates|
| addresses      | idx_addresses_customer             | B-Tree    | Customer address lookup         |
| reviews        | idx_reviews_product                | B-Tree    | Product review listing          |
| reviews        | uq_reviews_product_customer        | Unique    | One review per product/customer |
| inventory_log  | idx_invlog_product_date            | Composite | Stock movement by product/date  |

---

## 6. Data Dictionary (Key Tables)

### products

| Column           | Type           | Nullable | Default  | Constraints        |
|------------------|----------------|----------|----------|--------------------|
| product_id       | INT            | NO       | AUTO_INC | PRIMARY KEY        |
| category_id      | INT            | NO       | —        | FOREIGN KEY        |
| supplier_id      | INT            | YES      | NULL     | FOREIGN KEY        |
| product_code     | VARCHAR(20)    | NO       | —        | UNIQUE             |
| product_name     | VARCHAR(255)   | NO       | —        |                    |
| description      | TEXT           | YES      | NULL     |                    |
| list_price       | DECIMAL(10,2)  | NO       | —        | CHECK (>= 0)      |
| cost_price       | DECIMAL(10,2)  | NO       | 0.00     | CHECK (>= 0)      |
| discount_percent | DECIMAL(5,2)   | NO       | 0.00     | CHECK (0-100)     |
| quantity_on_hand | INT            | NO       | 0        | CHECK (>= 0)      |
| reorder_point    | INT            | NO       | 10       |                    |
| date_added       | DATETIME       | NO       | NOW()    |                    |
| is_active        | BOOLEAN        | NO       | TRUE     |                    |

### orders

| Column          | Type           | Nullable | Default  | Constraints        |
|-----------------|----------------|----------|----------|--------------------|
| order_id        | INT            | NO       | AUTO_INC | PRIMARY KEY        |
| customer_id     | INT            | NO       | —        | FOREIGN KEY        |
| order_date      | DATETIME       | NO       | NOW()    |                    |
| ship_date       | DATETIME       | YES      | NULL     |                    |
| ship_amount     | DECIMAL(10,2)  | NO       | 0.00     |                    |
| tax_amount      | DECIMAL(10,2)  | NO       | 0.00     |                    |
| order_status    | ENUM           | NO       | 'pending'|                    |
| payment_type    | VARCHAR(20)    | NO       | —        |                    |
| card_last_four  | CHAR(4)        | YES      | NULL     |                    |

---

## 7. Sample Queries Enabled by This Design

```sql
-- Top 5 selling products (revenue)
SELECT p.product_name, SUM(oi.quantity) AS units,
       SUM((oi.item_price - oi.discount_amount) * oi.quantity) AS revenue
FROM order_items oi JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_id ORDER BY revenue DESC LIMIT 5;

-- Low stock alert
SELECT product_name, quantity_on_hand, reorder_point
FROM products WHERE quantity_on_hand <= reorder_point AND is_active = TRUE;

-- Customer lifetime value
SELECT c.first_name, c.last_name,
       COUNT(DISTINCT o.order_id) AS orders,
       SUM((oi.item_price - oi.discount_amount) * oi.quantity) AS ltv
FROM customers c JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id ORDER BY ltv DESC;
```
