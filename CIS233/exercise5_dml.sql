-- ============================================================
-- MySQL Exercise 5 — Insert, Update, and Delete Data
-- CIS 233 — Database Management | FLLC Enterprise
-- Author: Preston Furulie
-- Database: my_guitar_shop
-- ============================================================
-- Concepts: INSERT (auto-increment), UPDATE (single row,
--           all rows), DELETE (with foreign key constraints),
--           column lists, NOW(), safe-update mode
-- ============================================================
-- IMPORTANT: Run steps in order (1-9).
-- Step 10 restores the database to its original state.
-- ============================================================

USE my_guitar_shop;

-- ────────────────────────────────────────────────────────────
-- Step 1: INSERT a new category
-- Omitting category_id lets MySQL auto-generate it via
-- AUTO_INCREMENT. Only the category_name column is needed.
-- ────────────────────────────────────────────────────────────
INSERT INTO categories (category_name)
VALUES ('Brass');

-- Verify the insert
SELECT * FROM categories ORDER BY category_id;


-- ────────────────────────────────────────────────────────────
-- Step 2: UPDATE the new category name
-- Changes 'Brass' to 'Woodwinds' using the category_id
-- assigned by AUTO_INCREMENT in Step 1.
-- Note: category_id may vary; adjust if needed.
-- ────────────────────────────────────────────────────────────
UPDATE categories
SET category_name = 'Woodwinds'
WHERE category_id = 5;

-- Verify the update
SELECT * FROM categories WHERE category_id = 5;


-- ────────────────────────────────────────────────────────────
-- Step 3: DELETE the category added in Step 1
-- This is safe because no products reference this category.
-- If products existed with this category_id, the DELETE
-- would fail due to the foreign key constraint.
-- ────────────────────────────────────────────────────────────
DELETE FROM categories
WHERE category_id = 5;

-- Verify the delete
SELECT * FROM categories ORDER BY category_id;


-- ────────────────────────────────────────────────────────────
-- Step 4: INSERT a new product with a column list
-- Using a column list explicitly names which columns
-- receive values (best practice for clarity and safety).
-- product_id is omitted → auto-generated.
-- NOW() inserts the current date and time for date_added.
-- ────────────────────────────────────────────────────────────
INSERT INTO products
    (category_id, product_code, product_name, description,
     list_price, discount_percent, date_added)
VALUES
    (4, 'dgx_640', 'Yamaha DGX 640 88-Key Digital Piano',
     'Long description to come.', 799.99, 0, NOW());

-- Verify the insert
SELECT product_id, product_name, list_price, discount_percent, date_added
FROM products
WHERE product_code = 'dgx_640';


-- ────────────────────────────────────────────────────────────
-- Step 5: UPDATE the product's discount percentage
-- Changes discount_percent from 0 to 35 for the product
-- added in Step 4. Uses product_code to identify the row.
-- ────────────────────────────────────────────────────────────
UPDATE products
SET discount_percent = 35
WHERE product_code = 'dgx_640';

-- Verify the update
SELECT product_name, list_price, discount_percent,
       ROUND(list_price * (1 - discount_percent / 100), 2) AS sale_price
FROM products
WHERE product_code = 'dgx_640';


-- ────────────────────────────────────────────────────────────
-- Step 6: DELETE the Keyboards category
-- Cannot delete a category that has products (FK constraint).
-- Must first delete dependent rows in order_items (which
-- reference products), then delete the products themselves,
-- then delete the category.
-- Each statement ends with a semicolon for multi-statement
-- script execution.
-- ────────────────────────────────────────────────────────────

-- 6a: Delete order_items referencing Keyboards products
DELETE FROM order_items
WHERE product_id IN
    (SELECT product_id FROM products WHERE category_id = 4);

-- 6b: Delete all products in the Keyboards category
DELETE FROM products
WHERE category_id = 4;

-- 6c: Now safe to delete the category itself
DELETE FROM categories
WHERE category_id = 4;

-- Verify: category 4 should be gone
SELECT * FROM categories ORDER BY category_id;


-- ────────────────────────────────────────────────────────────
-- Step 7: INSERT a new customer with a column list
-- Using a column list for clarity. The password column
-- receives an empty string (not NULL).
-- customer_id is auto-generated.
-- ────────────────────────────────────────────────────────────
INSERT INTO customers
    (email_address, password, first_name, last_name)
VALUES
    ('rick@raven.com', '', 'Rick', 'Raven');

-- Verify the insert
SELECT customer_id, email_address, first_name, last_name
FROM customers
WHERE email_address = 'rick@raven.com';


-- ────────────────────────────────────────────────────────────
-- Step 8: UPDATE Rick Raven's password
-- Sets password to 'secret' using email_address to
-- identify the specific customer row.
-- ────────────────────────────────────────────────────────────
UPDATE customers
SET password = 'secret'
WHERE email_address = 'rick@raven.com';

-- Verify the update
SELECT email_address, password, first_name, last_name
FROM customers
WHERE email_address = 'rick@raven.com';


-- ────────────────────────────────────────────────────────────
-- Step 9: UPDATE all customer passwords to 'reset'
-- This updates every row in the customers table.
-- MySQL safe-update mode may block UPDATE without a WHERE
-- clause that uses a key column. Adding LIMIT 100 satisfies
-- this requirement while still updating all rows (since
-- the table has fewer than 100 customers).
-- ────────────────────────────────────────────────────────────
UPDATE customers
SET password = 'reset'
LIMIT 100;

-- Verify: all passwords should now be 'reset'
SELECT customer_id, email_address, password
FROM customers
ORDER BY customer_id;


-- ────────────────────────────────────────────────────────────
-- Step 10: Restore the database
-- Run the create_my_guitar_shop.sql script from the
-- mgs_ex_starts directory to reset all data to its
-- original state after completing the exercise.
-- ────────────────────────────────────────────────────────────
-- SOURCE mgs_ex_starts/create_my_guitar_shop.sql;

-- ============================================================
-- END OF EXERCISE 5
-- ============================================================
