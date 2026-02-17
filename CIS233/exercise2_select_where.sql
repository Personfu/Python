-- Exercise 2: SELECT & WHERE Clauses
-- CIS 233 — Database Management | Preston Furulie

USE my_guitar_shop;

-- Products over $500 sorted by price descending
SELECT product_name, list_price, discount_percent
FROM products
WHERE list_price > 500
ORDER BY list_price DESC;

-- Products with names containing 'Guitar'
SELECT product_name, list_price
FROM products
WHERE product_name LIKE '%Guitar%';

-- Products with discount between 10% and 30%
SELECT product_name, list_price, discount_percent
FROM products
WHERE discount_percent BETWEEN 10 AND 30
ORDER BY discount_percent DESC;

-- Customers from specific states
SELECT first_name, last_name, state
FROM customers c
    JOIN addresses a ON c.shipping_address_id = a.address_id
WHERE state IN ('CA', 'WA', 'OR')
ORDER BY state, last_name;
