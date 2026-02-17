-- =============================================================================
-- MySQL Exercise 5 - Step 6
-- Author: Preston Furulie
-- Database: my_guitar_shop
-- Description: DELETE the Keyboards category from the Categories table.
--              Since foreign key constraints exist, we must first delete
--              all products that belong to the Keyboards category (category_id = 4)
--              before we can delete the category itself.
-- =============================================================================

USE my_guitar_shop;

-- First, delete all products in the Keyboards category (category_id = 4)
-- This must be done before deleting the category due to foreign key constraints
DELETE FROM order_items
WHERE product_id IN
    (SELECT product_id FROM products WHERE category_id = 4);

DELETE FROM products
WHERE category_id = 4;

-- Now delete the Keyboards category itself
DELETE FROM categories
WHERE category_id = 4;

-- Verify both deletes were successful
SELECT *
FROM categories;

SELECT *
FROM products
WHERE category_id = 4;
