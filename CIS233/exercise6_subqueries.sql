-- Exercise 6: Subqueries & CTEs
-- CIS 233 — Database Management | Preston Furulie

USE my_guitar_shop;

-- Products priced above average
SELECT product_name, list_price
FROM products
WHERE list_price > (SELECT AVG(list_price) FROM products)
ORDER BY list_price DESC;

-- Customers who have placed orders (EXISTS)
SELECT first_name, last_name
FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o
    WHERE o.customer_id = c.customer_id
);

-- CTE: Top spending customers
WITH customer_totals AS (
    SELECT c.customer_id, c.first_name, c.last_name,
           SUM(oi.item_price * oi.quantity) AS total
    FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY c.customer_id
)
SELECT first_name, last_name, total
FROM customer_totals
WHERE total > (SELECT AVG(total) FROM customer_totals)
ORDER BY total DESC;
