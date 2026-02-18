-- ============================================================
-- Advanced Queries
-- CIS 276DA — Advanced SQL & Data Analytics | FLLC Enterprise
-- Author: Preston Furulie
-- Database: my_guitar_shop
-- ============================================================
-- Covers: multi-table JOINs (3+), correlated subqueries,
-- EXISTS / NOT EXISTS, CASE expressions, window functions,
-- recursive CTEs, and pivot/unpivot techniques.
-- ============================================================

USE my_guitar_shop;

-- ════════════════════════════════════════════════════════════
-- SECTION 1: COMPLEX MULTI-TABLE JOINS (3+ TABLES)
-- ════════════════════════════════════════════════════════════

-- 1a. Full order detail: customer → order → items → product → category
SELECT c.first_name,
       c.last_name,
       c.email_address,
       o.order_id,
       o.order_date,
       p.product_name,
       cat.category_name,
       oi.item_price,
       oi.discount_amount,
       oi.quantity,
       (oi.item_price - oi.discount_amount) * oi.quantity AS line_total
FROM customers c
    JOIN orders o       ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id    = oi.order_id
    JOIN products p     ON oi.product_id = p.product_id
    JOIN categories cat ON p.category_id = cat.category_id
ORDER BY o.order_date DESC, o.order_id, oi.item_id;

-- 1b. Customer shipping info with order totals
SELECT c.first_name,
       c.last_name,
       a.line1       AS ship_street,
       a.city        AS ship_city,
       a.state       AS ship_state,
       a.zip_code    AS ship_zip,
       COUNT(DISTINCT o.order_id)                                AS order_count,
       SUM((oi.item_price - oi.discount_amount) * oi.quantity)   AS lifetime_value
FROM customers c
    JOIN addresses a    ON c.shipping_address_id = a.address_id
    JOIN orders o       ON c.customer_id         = o.customer_id
    JOIN order_items oi ON o.order_id            = oi.order_id
GROUP BY c.customer_id, c.first_name, c.last_name,
         a.line1, a.city, a.state, a.zip_code
ORDER BY lifetime_value DESC;

-- 1c. Products never ordered (LEFT JOIN chain)
SELECT p.product_id,
       p.product_name,
       cat.category_name,
       p.list_price
FROM products p
    JOIN categories cat  ON p.category_id = cat.category_id
    LEFT JOIN order_items oi ON p.product_id = oi.product_id
WHERE oi.item_id IS NULL
ORDER BY p.list_price DESC;


-- ════════════════════════════════════════════════════════════
-- SECTION 2: CORRELATED SUBQUERIES
-- ════════════════════════════════════════════════════════════

-- 2a. Products priced above their category average
SELECT p.product_name,
       p.list_price,
       cat.category_name,
       (SELECT AVG(p2.list_price)
        FROM products p2
        WHERE p2.category_id = p.category_id) AS category_avg
FROM products p
    JOIN categories cat ON p.category_id = cat.category_id
WHERE p.list_price > (SELECT AVG(p2.list_price)
                      FROM products p2
                      WHERE p2.category_id = p.category_id)
ORDER BY cat.category_name, p.list_price DESC;

-- 2b. Each customer's most recent order date and total
SELECT c.first_name,
       c.last_name,
       (SELECT MAX(o.order_date)
        FROM orders o
        WHERE o.customer_id = c.customer_id) AS latest_order,
       (SELECT SUM((oi.item_price - oi.discount_amount) * oi.quantity)
        FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.customer_id = c.customer_id) AS total_spent
FROM customers c
ORDER BY total_spent DESC;


-- ════════════════════════════════════════════════════════════
-- SECTION 3: EXISTS AND NOT EXISTS
-- ════════════════════════════════════════════════════════════

-- 3a. Customers who have placed at least one order
SELECT c.customer_id,
       c.first_name,
       c.last_name,
       c.email_address
FROM customers c
WHERE EXISTS (SELECT 1
              FROM orders o
              WHERE o.customer_id = c.customer_id)
ORDER BY c.last_name, c.first_name;

-- 3b. Customers who have NEVER ordered
SELECT c.customer_id,
       c.first_name,
       c.last_name,
       c.email_address
FROM customers c
WHERE NOT EXISTS (SELECT 1
                  FROM orders o
                  WHERE o.customer_id = c.customer_id)
ORDER BY c.last_name;

-- 3c. Categories that contain at least one product over $1000
SELECT cat.category_id,
       cat.category_name
FROM categories cat
WHERE EXISTS (SELECT 1
              FROM products p
              WHERE p.category_id = cat.category_id
                AND p.list_price > 1000);


-- ════════════════════════════════════════════════════════════
-- SECTION 4: CASE EXPRESSIONS
-- ════════════════════════════════════════════════════════════

-- 4a. Simple CASE — map category IDs to tier labels
SELECT p.product_name,
       p.list_price,
       CASE p.category_id
           WHEN 1 THEN 'Primary'
           WHEN 2 THEN 'Secondary'
           WHEN 3 THEN 'Accessories'
           ELSE        'Other'
       END AS category_tier
FROM products p
ORDER BY category_tier, p.product_name;

-- 4b. Searched CASE — price range classification
SELECT p.product_name,
       p.list_price,
       CASE
           WHEN p.list_price >= 2000 THEN 'Premium'
           WHEN p.list_price >= 1000 THEN 'Professional'
           WHEN p.list_price >= 500  THEN 'Intermediate'
           WHEN p.list_price >= 100  THEN 'Entry Level'
           ELSE                           'Budget'
       END AS price_tier
FROM products p
ORDER BY p.list_price DESC;

-- 4c. CASE inside aggregate — conditional counting
SELECT cat.category_name,
       COUNT(*)                                                    AS total_products,
       SUM(CASE WHEN p.list_price >= 1000 THEN 1 ELSE 0 END)     AS premium_count,
       SUM(CASE WHEN p.list_price < 1000 THEN 1 ELSE 0 END)      AS standard_count,
       ROUND(AVG(p.list_price), 2)                                 AS avg_price
FROM products p
    JOIN categories cat ON p.category_id = cat.category_id
GROUP BY cat.category_name
ORDER BY avg_price DESC;

-- 4d. Order shipping status with days elapsed
SELECT o.order_id,
       o.order_date,
       o.ship_date,
       CASE
           WHEN o.ship_date IS NOT NULL
               THEN CONCAT('Shipped (', DATEDIFF(o.ship_date, o.order_date), ' days)')
           WHEN DATEDIFF(NOW(), o.order_date) > 30
               THEN 'OVERDUE — Not Shipped'
           ELSE 'Processing'
       END AS fulfillment_status
FROM orders o
ORDER BY o.order_date DESC;


-- ════════════════════════════════════════════════════════════
-- SECTION 5: WINDOW FUNCTIONS
-- ════════════════════════════════════════════════════════════

-- 5a. ROW_NUMBER — sequential ranking within each category
SELECT ROW_NUMBER() OVER (PARTITION BY p.category_id
                          ORDER BY p.list_price DESC) AS rank_in_category,
       cat.category_name,
       p.product_name,
       p.list_price
FROM products p
    JOIN categories cat ON p.category_id = cat.category_id;

-- 5b. RANK vs DENSE_RANK — handling ties in global price ranking
SELECT p.product_name,
       p.list_price,
       RANK()       OVER (ORDER BY p.list_price DESC) AS price_rank,
       DENSE_RANK() OVER (ORDER BY p.list_price DESC) AS price_dense_rank
FROM products p;

-- 5c. LAG and LEAD — compare each product to its neighbors by price
SELECT p.product_name,
       p.list_price,
       LAG(p.list_price, 1)  OVER (ORDER BY p.list_price) AS prev_price,
       LEAD(p.list_price, 1) OVER (ORDER BY p.list_price) AS next_price,
       p.list_price - LAG(p.list_price, 1) OVER (ORDER BY p.list_price) AS price_gap
FROM products p;

-- 5d. NTILE — divide products into quartiles by price
SELECT p.product_name,
       p.list_price,
       NTILE(4) OVER (ORDER BY p.list_price) AS price_quartile
FROM products p;

-- 5e. Running total of order amounts by date
SELECT o.order_id,
       o.order_date,
       SUM((oi.item_price - oi.discount_amount) * oi.quantity) AS order_total,
       SUM(SUM((oi.item_price - oi.discount_amount) * oi.quantity))
           OVER (ORDER BY o.order_date
                 ROWS UNBOUNDED PRECEDING) AS running_total
FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, o.order_date
ORDER BY o.order_date;

-- 5f. Percentage of category total per product
SELECT cat.category_name,
       p.product_name,
       p.list_price,
       SUM(p.list_price) OVER (PARTITION BY p.category_id) AS category_total,
       ROUND(p.list_price * 100.0
             / SUM(p.list_price) OVER (PARTITION BY p.category_id), 2) AS pct_of_category
FROM products p
    JOIN categories cat ON p.category_id = cat.category_id
ORDER BY cat.category_name, pct_of_category DESC;


-- ════════════════════════════════════════════════════════════
-- SECTION 6: COMMON TABLE EXPRESSIONS (RECURSIVE CTEs)
-- ════════════════════════════════════════════════════════════

-- 6a. Basic CTE — top customers by spend
WITH customer_spend AS (
    SELECT c.customer_id,
           c.first_name,
           c.last_name,
           SUM((oi.item_price - oi.discount_amount) * oi.quantity) AS total_spent
    FROM customers c
        JOIN orders o       ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id    = oi.order_id
    GROUP BY c.customer_id, c.first_name, c.last_name
)
SELECT first_name,
       last_name,
       total_spent,
       RANK() OVER (ORDER BY total_spent DESC) AS spend_rank
FROM customer_spend;

-- 6b. Multi-CTE — category performance dashboard
WITH category_revenue AS (
    SELECT cat.category_id,
           cat.category_name,
           SUM((oi.item_price - oi.discount_amount) * oi.quantity) AS revenue
    FROM categories cat
        JOIN products p     ON cat.category_id = p.category_id
        JOIN order_items oi ON p.product_id    = oi.product_id
    GROUP BY cat.category_id, cat.category_name
),
overall AS (
    SELECT SUM(revenue) AS total_revenue
    FROM category_revenue
)
SELECT cr.category_name,
       cr.revenue,
       ROUND(cr.revenue * 100.0 / o.total_revenue, 2) AS pct_of_total,
       RANK() OVER (ORDER BY cr.revenue DESC)          AS revenue_rank
FROM category_revenue cr
    CROSS JOIN overall o
ORDER BY cr.revenue DESC;

-- 6c. Recursive CTE — generate a numeric sequence (1..20)
WITH RECURSIVE num_seq AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1
    FROM num_seq
    WHERE n < 20
)
SELECT n FROM num_seq;

-- 6d. Recursive CTE — price bracket histogram
WITH RECURSIVE price_brackets AS (
    SELECT 0    AS bracket_low,
           249  AS bracket_high
    UNION ALL
    SELECT bracket_low + 250,
           bracket_high + 250
    FROM price_brackets
    WHERE bracket_high < 5000
),
product_counts AS (
    SELECT pb.bracket_low,
           pb.bracket_high,
           COUNT(p.product_id) AS product_count
    FROM price_brackets pb
        LEFT JOIN products p
            ON p.list_price >= pb.bracket_low
           AND p.list_price <= pb.bracket_high
    GROUP BY pb.bracket_low, pb.bracket_high
)
SELECT CONCAT('$', bracket_low, ' - $', bracket_high) AS price_range,
       product_count,
       REPEAT('█', product_count) AS histogram
FROM product_counts
ORDER BY bracket_low;


-- ════════════════════════════════════════════════════════════
-- SECTION 7: PIVOT / UNPIVOT TECHNIQUES
-- ════════════════════════════════════════════════════════════

-- 7a. Pivot — orders per category per month (manual pivot in MySQL)
SELECT DATE_FORMAT(o.order_date, '%Y-%m') AS order_month,
       SUM(CASE WHEN cat.category_name = 'Guitars'
                THEN (oi.item_price - oi.discount_amount) * oi.quantity ELSE 0 END) AS guitars_revenue,
       SUM(CASE WHEN cat.category_name = 'Basses'
                THEN (oi.item_price - oi.discount_amount) * oi.quantity ELSE 0 END) AS basses_revenue,
       SUM(CASE WHEN cat.category_name = 'Drums'
                THEN (oi.item_price - oi.discount_amount) * oi.quantity ELSE 0 END) AS drums_revenue,
       SUM((oi.item_price - oi.discount_amount) * oi.quantity)                      AS total_revenue
FROM orders o
    JOIN order_items oi ON o.order_id    = oi.order_id
    JOIN products p     ON oi.product_id = p.product_id
    JOIN categories cat ON p.category_id = cat.category_id
GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
ORDER BY order_month;

-- 7b. Unpivot — turn columnar address fields into rows
SELECT c.customer_id,
       c.first_name,
       c.last_name,
       'billing'  AS address_type,
       a.line1, a.city, a.state, a.zip_code
FROM customers c
    JOIN addresses a ON c.billing_address_id = a.address_id
UNION ALL
SELECT c.customer_id,
       c.first_name,
       c.last_name,
       'shipping' AS address_type,
       a.line1, a.city, a.state, a.zip_code
FROM customers c
    JOIN addresses a ON c.shipping_address_id = a.address_id
ORDER BY customer_id, address_type;

-- 7c. Cross-tab summary — product count by category and price tier
SELECT cat.category_name,
       SUM(CASE WHEN p.list_price < 500                       THEN 1 ELSE 0 END) AS under_500,
       SUM(CASE WHEN p.list_price >= 500  AND p.list_price < 1000  THEN 1 ELSE 0 END) AS '500_to_999',
       SUM(CASE WHEN p.list_price >= 1000 AND p.list_price < 2000  THEN 1 ELSE 0 END) AS '1000_to_1999',
       SUM(CASE WHEN p.list_price >= 2000                     THEN 1 ELSE 0 END) AS '2000_plus',
       COUNT(*) AS total
FROM products p
    JOIN categories cat ON p.category_id = cat.category_id
GROUP BY cat.category_name
ORDER BY total DESC;


-- ════════════════════════════════════════════════════════════
-- SECTION 8: COMBINED ANALYTICS — PUTTING IT ALL TOGETHER
-- ════════════════════════════════════════════════════════════

-- 8a. Customer RFM (Recency, Frequency, Monetary) analysis
WITH rfm_raw AS (
    SELECT c.customer_id,
           c.first_name,
           c.last_name,
           DATEDIFF(NOW(), MAX(o.order_date))                       AS recency_days,
           COUNT(DISTINCT o.order_id)                                AS frequency,
           SUM((oi.item_price - oi.discount_amount) * oi.quantity)   AS monetary
    FROM customers c
        JOIN orders o       ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id    = oi.order_id
    GROUP BY c.customer_id, c.first_name, c.last_name
)
SELECT first_name,
       last_name,
       recency_days,
       frequency,
       ROUND(monetary, 2) AS monetary,
       NTILE(5) OVER (ORDER BY recency_days ASC)  AS r_score,
       NTILE(5) OVER (ORDER BY frequency DESC)     AS f_score,
       NTILE(5) OVER (ORDER BY monetary DESC)      AS m_score
FROM rfm_raw
ORDER BY monetary DESC;

-- 8b. Year-over-year growth by category
WITH yearly AS (
    SELECT cat.category_name,
           YEAR(o.order_date) AS order_year,
           SUM((oi.item_price - oi.discount_amount) * oi.quantity) AS annual_revenue
    FROM categories cat
        JOIN products p     ON cat.category_id = p.category_id
        JOIN order_items oi ON p.product_id    = oi.product_id
        JOIN orders o       ON oi.order_id     = o.order_id
    GROUP BY cat.category_name, YEAR(o.order_date)
)
SELECT category_name,
       order_year,
       annual_revenue,
       LAG(annual_revenue) OVER (PARTITION BY category_name ORDER BY order_year) AS prev_year_revenue,
       ROUND((annual_revenue - LAG(annual_revenue)
              OVER (PARTITION BY category_name ORDER BY order_year))
             * 100.0
             / NULLIF(LAG(annual_revenue)
                      OVER (PARTITION BY category_name ORDER BY order_year), 0), 2) AS yoy_growth_pct
FROM yearly
ORDER BY category_name, order_year;
