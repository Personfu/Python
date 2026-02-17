-- ============================================================
-- MySQL Exercise 4 — Retrieve Data from Two or More Tables
-- CIS 233 — Database Management | FLLC Enterprise
-- Author: Preston Furulie
-- Database: my_guitar_shop
-- ============================================================
-- Concepts: INNER JOIN, LEFT OUTER JOIN, self-join, UNION,
--           table aliases, multi-table joins, qualified columns
-- ============================================================

USE my_guitar_shop;

-- ────────────────────────────────────────────────────────────
-- Step 1: Join Categories to Products
-- INNER JOIN returns only rows with matching category_id
-- in both tables. Sorted by category then product name.
-- ────────────────────────────────────────────────────────────
SELECT c.category_name,
       p.product_name,
       p.list_price
FROM categories c
    JOIN products p
        ON c.category_id = p.category_id
ORDER BY c.category_name, p.product_name;


-- ────────────────────────────────────────────────────────────
-- Step 2: Customer addresses for allan.sherwood@yahoo.com
-- Joins Customers to Addresses on customer_id.
-- WHERE clause filters to a single customer by email.
-- Returns one row per address for that customer.
-- ────────────────────────────────────────────────────────────
SELECT c.first_name,
       c.last_name,
       a.line1,
       a.city,
       a.state,
       a.zip_code
FROM customers c
    JOIN addresses a
        ON c.customer_id = a.customer_id
WHERE c.email_address = 'allan.sherwood@yahoo.com';


-- ────────────────────────────────────────────────────────────
-- Step 3: Customer shipping addresses only
-- Instead of joining on customer_id (all addresses),
-- we join on shipping_address_id to get only the
-- designated shipping address for each customer.
-- ────────────────────────────────────────────────────────────
SELECT c.first_name,
       c.last_name,
       a.line1,
       a.city,
       a.state,
       a.zip_code
FROM customers c
    JOIN addresses a
        ON c.shipping_address_id = a.address_id;


-- ────────────────────────────────────────────────────────────
-- Step 4: Four-table JOIN with aliases
-- Joins: Customers → Orders → Order_Items → Products
-- Aliases: c (customers), o (orders), oi (order_items), p (products)
-- This traces the full order chain from customer to product.
-- ────────────────────────────────────────────────────────────
SELECT c.last_name,
       c.first_name,
       o.order_date,
       p.product_name,
       oi.item_price,
       oi.discount_amount,
       oi.quantity
FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN order_items oi
        ON o.order_id = oi.order_id
    JOIN products p
        ON oi.product_id = p.product_id
ORDER BY c.last_name, o.order_date, p.product_name;


-- ────────────────────────────────────────────────────────────
-- Step 5: Self-join — products with the same list price
-- A self-join compares a table to itself using two aliases.
-- p1.product_id != p2.product_id ensures we don't match
-- a product with itself, while p1.list_price = p2.list_price
-- finds products sharing the same price.
-- DISTINCT prevents duplicate rows.
-- ────────────────────────────────────────────────────────────
SELECT DISTINCT p1.product_name,
                p1.list_price
FROM products p1
    JOIN products p2
        ON p1.product_id != p2.product_id
        AND p1.list_price = p2.list_price
ORDER BY p1.product_name;


-- ────────────────────────────────────────────────────────────
-- Step 6: LEFT OUTER JOIN — unused categories
-- LEFT JOIN returns ALL categories, even those with no
-- matching products. We then filter with WHERE p.product_id
-- IS NULL to find categories that have never been assigned
-- to any product.
-- ────────────────────────────────────────────────────────────
SELECT c.category_name,
       p.product_id
FROM categories c
    LEFT JOIN products p
        ON c.category_id = p.category_id
WHERE p.product_id IS NULL;


-- ────────────────────────────────────────────────────────────
-- Step 7: UNION — shipping status report
-- UNION combines two SELECT statements into one result set.
-- First query: orders that HAVE a ship_date → 'SHIPPED'
-- Second query: orders with NULL ship_date → 'NOT SHIPPED'
-- The calculated column ship_status is created using
-- string literals in the SELECT clause.
-- ORDER BY applies to the combined result.
-- ────────────────────────────────────────────────────────────
SELECT 'SHIPPED' AS ship_status,
       order_id,
       order_date
FROM orders
WHERE ship_date IS NOT NULL

UNION

SELECT 'NOT SHIPPED' AS ship_status,
       order_id,
       order_date
FROM orders
WHERE ship_date IS NULL

ORDER BY order_date;

-- ============================================================
-- END OF EXERCISE 4
-- ============================================================
