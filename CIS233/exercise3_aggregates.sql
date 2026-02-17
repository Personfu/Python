-- ============================================================
-- Exercise 3: Aggregate Functions & GROUP BY — Complete
-- CIS 233 — Database Management | Preston Furulie
-- Database: my_guitar_shop
-- ============================================================
-- Covers: COUNT, SUM, AVG, MIN, MAX, GROUP BY, HAVING,
-- GROUP BY with JOINs, multiple aggregates, ROLLUP,
-- conditional aggregation (CASE), and date functions.
-- ============================================================

USE my_guitar_shop;

-- ── 1. Basic Aggregate Functions ───────────────────────────

-- Count all products
SELECT COUNT(*) AS total_products
FROM products;

-- Sum of all list prices
SELECT SUM(list_price) AS total_catalog_value
FROM products;

-- Average, min, max price
SELECT AVG(list_price)  AS avg_price,
       MIN(list_price)  AS min_price,
       MAX(list_price)  AS max_price,
       MAX(list_price) - MIN(list_price) AS price_range
FROM products;


-- ── 2. COUNT Variations ────────────────────────────────────

-- COUNT(*) counts all rows (including NULLs)
-- COUNT(column) counts non-NULL values in that column
-- COUNT(DISTINCT column) counts unique non-NULL values

SELECT COUNT(*)              AS total_orders,
       COUNT(ship_date)      AS shipped_orders,
       COUNT(*) - COUNT(ship_date) AS pending_orders
FROM orders;

-- Count distinct categories that have products
SELECT COUNT(DISTINCT category_id) AS active_categories
FROM products;


-- ── 3. GROUP BY ────────────────────────────────────────────

-- Product count and pricing stats per category
SELECT c.category_name,
       COUNT(*)                AS product_count,
       ROUND(AVG(p.list_price), 2) AS avg_price,
       MIN(p.list_price)       AS cheapest,
       MAX(p.list_price)       AS most_expensive,
       SUM(p.list_price)       AS total_value
FROM categories c
    JOIN products p ON c.category_id = p.category_id
GROUP BY c.category_name
ORDER BY product_count DESC;


-- ── 4. HAVING (Filter on Aggregate Results) ────────────────

-- Categories with more than 2 products
SELECT c.category_name,
       COUNT(*) AS product_count
FROM categories c
    JOIN products p ON c.category_id = p.category_id
GROUP BY c.category_name
HAVING product_count > 2
ORDER BY product_count DESC;

-- Total revenue per customer, only showing those who spent > $200
SELECT c.last_name, c.first_name,
       SUM((oi.item_price - oi.discount_amount) * oi.quantity) AS total_spent
FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.last_name, c.first_name
HAVING total_spent > 200
ORDER BY total_spent DESC;


-- ── 5. GROUP BY with Multiple Columns ──────────────────────

-- Orders per customer per year
SELECT c.last_name, c.first_name,
       YEAR(o.order_date)   AS order_year,
       COUNT(*)              AS order_count,
       SUM((oi.item_price - oi.discount_amount) * oi.quantity) AS total_spent
FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.last_name, c.first_name, YEAR(o.order_date)
ORDER BY c.last_name, order_year;


-- ── 6. Conditional Aggregation (CASE inside aggregate) ─────

-- Count products in price tiers
SELECT
    COUNT(CASE WHEN list_price < 100 THEN 1 END)         AS budget,
    COUNT(CASE WHEN list_price BETWEEN 100 AND 499 THEN 1 END) AS mid_range,
    COUNT(CASE WHEN list_price BETWEEN 500 AND 999 THEN 1 END) AS premium,
    COUNT(CASE WHEN list_price >= 1000 THEN 1 END)        AS luxury
FROM products;

-- Revenue by shipping status
SELECT
    SUM(CASE WHEN o.ship_date IS NOT NULL
         THEN (oi.item_price - oi.discount_amount) * oi.quantity
         ELSE 0 END) AS shipped_revenue,
    SUM(CASE WHEN o.ship_date IS NULL
         THEN (oi.item_price - oi.discount_amount) * oi.quantity
         ELSE 0 END) AS pending_revenue
FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id;


-- ── 7. Date Functions with Aggregation ─────────────────────

-- Order count by month
SELECT YEAR(order_date)  AS yr,
       MONTH(order_date) AS mo,
       COUNT(*)           AS order_count
FROM orders
GROUP BY YEAR(order_date), MONTH(order_date)
ORDER BY yr, mo;

-- Average days to ship
SELECT ROUND(AVG(DATEDIFF(ship_date, order_date)), 1) AS avg_days_to_ship
FROM orders
WHERE ship_date IS NOT NULL;


-- ── 8. GROUP BY with ROLLUP (Subtotals) ────────────────────

-- Category sales with grand total
SELECT COALESCE(c.category_name, '** GRAND TOTAL **') AS category,
       COUNT(*)                                        AS items_sold,
       SUM((oi.item_price - oi.discount_amount) * oi.quantity) AS revenue
FROM categories c
    JOIN products p ON c.category_id = p.category_id
    JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY c.category_name WITH ROLLUP;


-- ── 9. Aggregate Subquery ──────────────────────────────────

-- Products priced above the overall average
SELECT product_name, list_price,
       list_price - (SELECT AVG(list_price) FROM products) AS above_avg_by
FROM products
WHERE list_price > (SELECT AVG(list_price) FROM products)
ORDER BY list_price DESC;
