-- ============================================================
-- Exercise 6: Subqueries & CTEs — Complete
-- CIS 233 — Database Management | Preston Furulie
-- Database: my_guitar_shop
-- ============================================================
-- Covers: scalar subqueries, column subqueries (IN, ANY, ALL),
-- correlated subqueries, EXISTS/NOT EXISTS, subqueries in
-- FROM clause (derived tables), Common Table Expressions (CTEs),
-- recursive CTEs, and practical applications.
-- ============================================================

USE my_guitar_shop;

-- ── 1. Scalar Subquery (Returns Single Value) ──────────────

-- Products priced above the overall average
SELECT product_name, list_price
FROM products
WHERE list_price > (SELECT AVG(list_price) FROM products)
ORDER BY list_price DESC;

-- Most recent order
SELECT order_id, customer_id, order_date
FROM orders
WHERE order_date = (SELECT MAX(order_date) FROM orders);


-- ── 2. Column Subquery with IN ─────────────────────────────

-- Customers who have placed at least one order
SELECT first_name, last_name, email_address
FROM customers
WHERE customer_id IN (
    SELECT DISTINCT customer_id FROM orders
)
ORDER BY last_name;

-- Products that have never been ordered
SELECT product_name, list_price
FROM products
WHERE product_id NOT IN (
    SELECT DISTINCT product_id FROM order_items
);


-- ── 3. ANY and ALL ─────────────────────────────────────────

-- Products cheaper than ANY product in category 1
-- (i.e., cheaper than the most expensive in category 1)
SELECT product_name, list_price, category_id
FROM products
WHERE list_price < ANY (
    SELECT list_price FROM products WHERE category_id = 1
)
ORDER BY list_price;

-- Products more expensive than ALL products in category 2
-- (i.e., more expensive than the most expensive in category 2)
SELECT product_name, list_price
FROM products
WHERE list_price > ALL (
    SELECT list_price FROM products WHERE category_id = 2
)
ORDER BY list_price;


-- ── 4. Correlated Subquery ─────────────────────────────────
-- The inner query references a column from the outer query,
-- so it executes once per row of the outer query.

-- Products with list_price above their category's average
SELECT p.product_name, p.list_price, p.category_id
FROM products p
WHERE p.list_price > (
    SELECT AVG(p2.list_price)
    FROM products p2
    WHERE p2.category_id = p.category_id
)
ORDER BY p.category_id, p.list_price DESC;


-- ── 5. EXISTS / NOT EXISTS ─────────────────────────────────
-- EXISTS returns TRUE if the subquery returns any rows.
-- More efficient than IN for large datasets.

-- Customers who have placed orders (EXISTS)
SELECT c.first_name, c.last_name
FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o
    WHERE o.customer_id = c.customer_id
)
ORDER BY c.last_name;

-- Categories that have NO products (NOT EXISTS)
SELECT c.category_name
FROM categories c
WHERE NOT EXISTS (
    SELECT 1 FROM products p
    WHERE p.category_id = c.category_id
);


-- ── 6. Subquery in FROM (Derived Table) ────────────────────

-- Average order total per customer, then find above-average spenders
SELECT d.first_name, d.last_name, d.total_spent
FROM (
    SELECT c.customer_id, c.first_name, c.last_name,
           SUM((oi.item_price - oi.discount_amount) * oi.quantity) AS total_spent
    FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY c.customer_id, c.first_name, c.last_name
) AS d
WHERE d.total_spent > (
    SELECT AVG(sub.total)
    FROM (
        SELECT SUM((oi2.item_price - oi2.discount_amount) * oi2.quantity) AS total
        FROM orders o2
            JOIN order_items oi2 ON o2.order_id = oi2.order_id
        GROUP BY o2.customer_id
    ) AS sub
)
ORDER BY d.total_spent DESC;


-- ── 7. Subquery in SELECT (Scalar Column) ──────────────────

-- Each product with its category's average price for comparison
SELECT p.product_name,
       p.list_price,
       (SELECT AVG(p2.list_price)
        FROM products p2
        WHERE p2.category_id = p.category_id) AS category_avg,
       p.list_price - (SELECT AVG(p2.list_price)
                        FROM products p2
                        WHERE p2.category_id = p.category_id) AS diff_from_avg
FROM products p
ORDER BY diff_from_avg DESC;


-- ── 8. Common Table Expressions (CTEs) ─────────────────────
-- CTEs are named temporary result sets that make complex
-- queries more readable. Defined with WITH ... AS.

-- CTE: Top spending customers
WITH customer_totals AS (
    SELECT c.customer_id,
           c.first_name,
           c.last_name,
           SUM((oi.item_price - oi.discount_amount) * oi.quantity) AS total,
           COUNT(DISTINCT o.order_id) AS order_count
    FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY c.customer_id, c.first_name, c.last_name
)
SELECT first_name, last_name, total, order_count,
       ROUND(total / order_count, 2) AS avg_order_value
FROM customer_totals
WHERE total > (SELECT AVG(total) FROM customer_totals)
ORDER BY total DESC;

-- Multiple CTEs in one query
WITH category_stats AS (
    SELECT c.category_id, c.category_name,
           COUNT(*) AS product_count,
           AVG(p.list_price) AS avg_price
    FROM categories c
        JOIN products p ON c.category_id = p.category_id
    GROUP BY c.category_id, c.category_name
),
order_stats AS (
    SELECT p.category_id,
           SUM(oi.quantity) AS units_sold,
           SUM((oi.item_price - oi.discount_amount) * oi.quantity) AS revenue
    FROM products p
        JOIN order_items oi ON p.product_id = oi.product_id
    GROUP BY p.category_id
)
SELECT cs.category_name,
       cs.product_count,
       ROUND(cs.avg_price, 2) AS avg_price,
       COALESCE(os.units_sold, 0) AS units_sold,
       COALESCE(ROUND(os.revenue, 2), 0) AS revenue
FROM category_stats cs
    LEFT JOIN order_stats os ON cs.category_id = os.category_id
ORDER BY revenue DESC;
