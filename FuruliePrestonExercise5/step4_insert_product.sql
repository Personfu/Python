-- =============================================================================
-- MySQL Exercise 5 - Step 4
-- Author: Preston Furulie
-- Database: my_guitar_shop
-- Description: INSERT a new product into the Products table using a
--              column list. The product_id is auto-generated. The
--              date_added column uses the NOW() function for today's
--              date/time.
-- =============================================================================

USE my_guitar_shop;

-- Insert the new product with a column list
INSERT INTO products
    (category_id, product_code, product_name, description,
     list_price, discount_percent, date_added)
VALUES
    (4, 'dgx_640', 'Yamaha DGX 640 88-Key Digital Piano',
     'Long description to come.', 799.99, 0, NOW());

-- Verify the insert was successful
SELECT *
FROM products
WHERE product_code = 'dgx_640';
