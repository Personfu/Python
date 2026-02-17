-- ============================================================
-- Exercise 2: SELECT & WHERE Clauses — Complete
-- CIS 233 — Database Management | Preston Furulie
-- Database: my_guitar_shop
-- ============================================================
-- Covers: SELECT, FROM, WHERE, ORDER BY, LIMIT, DISTINCT,
-- comparison operators (=, <>, >, <, >=, <=), BETWEEN, IN,
-- LIKE with wildcards, IS NULL/IS NOT NULL, AND/OR/NOT,
-- column aliases, calculated columns, and string functions.
-- ============================================================

USE my_guitar_shop;

-- ── 1. Basic SELECT with WHERE ─────────────────────────────

-- Products over $500 sorted by price descending
SELECT product_name, list_price, discount_percent
FROM products
WHERE list_price > 500
ORDER BY list_price DESC;

-- Products with a specific discount percentage
SELECT product_name, list_price, discount_percent
FROM products
WHERE discount_percent = 30;


-- ── 2. Comparison Operators ────────────────────────────────

-- Not equal: products NOT in category 1
SELECT product_name, category_id, list_price
FROM products
WHERE category_id <> 1;

-- Greater than or equal to
SELECT product_name, list_price
FROM products
WHERE list_price >= 1000
ORDER BY list_price;


-- ── 3. BETWEEN (Inclusive Range) ───────────────────────────

-- Products priced between $100 and $500
SELECT product_name, list_price
FROM products
WHERE list_price BETWEEN 100 AND 500
ORDER BY list_price;

-- Discount between 10% and 30%
SELECT product_name, list_price, discount_percent
FROM products
WHERE discount_percent BETWEEN 10 AND 30
ORDER BY discount_percent DESC;


-- ── 4. IN (Set Membership) ─────────────────────────────────

-- Products in categories 1 or 2
SELECT product_name, category_id, list_price
FROM products
WHERE category_id IN (1, 2)
ORDER BY category_id, product_name;


-- ── 5. LIKE (Pattern Matching) ─────────────────────────────
-- % = any number of characters (including zero)
-- _ = exactly one character

-- Products containing 'Guitar' anywhere in the name
SELECT product_name, list_price
FROM products
WHERE product_name LIKE '%Guitar%';

-- Products starting with 'Fender'
SELECT product_name, list_price
FROM products
WHERE product_name LIKE 'Fender%';

-- Products with exactly 5 characters in the product code
SELECT product_code, product_name
FROM products
WHERE product_code LIKE '_____';


-- ── 6. IS NULL / IS NOT NULL ───────────────────────────────

-- Orders that have NOT been shipped (ship_date is NULL)
SELECT order_id, order_date, ship_date
FROM orders
WHERE ship_date IS NULL;

-- Orders that HAVE been shipped
SELECT order_id, order_date, ship_date
FROM orders
WHERE ship_date IS NOT NULL
ORDER BY ship_date DESC;


-- ── 7. Compound Conditions (AND, OR, NOT) ──────────────────

-- Products over $500 AND with discount > 10%
SELECT product_name, list_price, discount_percent
FROM products
WHERE list_price > 500
  AND discount_percent > 10
ORDER BY list_price DESC;

-- Products in category 1 OR priced under $100
SELECT product_name, category_id, list_price
FROM products
WHERE category_id = 1
   OR list_price < 100;

-- Products NOT in category 1
SELECT product_name, category_id
FROM products
WHERE NOT category_id = 1;


-- ── 8. Calculated Columns & Aliases ────────────────────────

-- Calculate discounted price using column alias
SELECT product_name,
       list_price,
       discount_percent,
       list_price * (discount_percent / 100) AS discount_amount,
       list_price - (list_price * discount_percent / 100) AS sale_price
FROM products
ORDER BY sale_price DESC;

-- Total order value
SELECT order_id,
       item_price,
       discount_amount,
       quantity,
       (item_price - discount_amount) * quantity AS total_line_value
FROM order_items
ORDER BY total_line_value DESC;


-- ── 9. DISTINCT (Remove Duplicates) ────────────────────────

-- Unique states from addresses
SELECT DISTINCT state
FROM addresses
ORDER BY state;

-- Unique discount percentages
SELECT DISTINCT discount_percent
FROM products
ORDER BY discount_percent;


-- ── 10. LIMIT and OFFSET ──────────────────────────────────

-- Top 5 most expensive products
SELECT product_name, list_price
FROM products
ORDER BY list_price DESC
LIMIT 5;

-- Products 6-10 (pagination: page 2 with 5 per page)
SELECT product_name, list_price
FROM products
ORDER BY list_price DESC
LIMIT 5 OFFSET 5;


-- ── 11. String Functions ───────────────────────────────────

-- Concatenation, upper/lower, length
SELECT product_name,
       UPPER(product_name)              AS upper_name,
       LOWER(product_name)              AS lower_name,
       LENGTH(product_name)             AS name_length,
       CONCAT(product_name, ' ($', list_price, ')') AS display_name
FROM products
ORDER BY name_length DESC;


-- ── 12. JOIN with WHERE (from Exercise 4 preview) ──────────

-- Customers from specific states
SELECT c.first_name, c.last_name, a.state, a.city
FROM customers c
    JOIN addresses a ON c.shipping_address_id = a.address_id
WHERE a.state IN ('CA', 'WA', 'OR')
ORDER BY a.state, c.last_name;
