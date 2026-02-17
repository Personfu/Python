-- MySQL Exercise 5 - Preston Furulie
-- Database: my_guitar_shop
-- Run steps in order (1-9), then run Step 10 to restore the database.

USE my_guitar_shop;

-- Step 1: Insert a new category
INSERT INTO categories (category_name)
VALUES ('Brass');

-- Step 2: Update the new category to Woodwinds
UPDATE categories
SET category_name = 'Woodwinds'
WHERE category_id = 5;

-- Step 3: Delete the new category
DELETE FROM categories
WHERE category_id = 5;

-- Step 4: Insert a new product using a column list
INSERT INTO products
    (category_id, product_code, product_name, description,
     list_price, discount_percent, date_added)
VALUES
    (4, 'dgx_640', 'Yamaha DGX 640 88-Key Digital Piano',
     'Long description to come.', 799.99, 0, NOW());

-- Step 5: Update the new product's discount to 35%
UPDATE products
SET discount_percent = 35
WHERE product_code = 'dgx_640';

-- Step 6: Delete the Keyboards category (must delete products first)
DELETE FROM order_items
WHERE product_id IN
    (SELECT product_id FROM products WHERE category_id = 4);

DELETE FROM products
WHERE category_id = 4;

DELETE FROM categories
WHERE category_id = 4;

-- Step 7: Insert a new customer using a column list
INSERT INTO customers
    (email_address, password, first_name, last_name)
VALUES
    ('rick@raven.com', '', 'Rick', 'Raven');

-- Step 8: Update Rick Raven's password to secret
UPDATE customers
SET password = 'secret'
WHERE email_address = 'rick@raven.com';

-- Step 9: Update all customer passwords to reset
UPDATE customers
SET password = 'reset'
LIMIT 100;

-- Step 10: Restore the database
-- Open and run create_my_guitar_shop.sql from the mgs_ex_starts directory
