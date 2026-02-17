-- Exercise 3: Aggregate Functions & GROUP BY
-- CIS 233 — Database Management | Preston Furulie

USE my_guitar_shop;

-- Count products per category
SELECT c.category_name,
       COUNT(*) AS product_count,
       AVG(p.list_price) AS avg_price,
       MAX(p.list_price) AS max_price
FROM categories c
    JOIN products p ON c.category_id = p.category_id
GROUP BY c.category_name
ORDER BY product_count DESC;

-- Total revenue per customer (HAVING filter)
SELECT c.last_name, c.first_name,
       SUM(oi.item_price * oi.quantity) AS total_spent
FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id
HAVING total_spent > 200
ORDER BY total_spent DESC;

-- Order count by year
SELECT YEAR(order_date) AS order_year,
       COUNT(*) AS order_count
FROM orders
GROUP BY YEAR(order_date)
ORDER BY order_year;
