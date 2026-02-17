-- =============================================================================
-- MySQL Exercise 5 - Step 5
-- Author: Preston Furulie
-- Database: my_guitar_shop
-- Description: UPDATE the product added in Step 4 to change the
--              discount_percent from 0% to 35%.
-- =============================================================================

USE my_guitar_shop;

-- Update the discount_percent for the Yamaha DGX 640
UPDATE products
SET discount_percent = 35
WHERE product_code = 'dgx_640';

-- Verify the update was successful
SELECT product_name, discount_percent
FROM products
WHERE product_code = 'dgx_640';
