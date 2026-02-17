-- =============================================================================
-- MySQL Exercise 4 - Step 1
-- Author: Preston Furulie
-- Database: my_guitar_shop
-- Description: INNER JOIN the Categories table to the Products table.
--              Returns category_name, product_name, and list_price.
--              Sorted by category_name, then product_name in ascending order.
-- =============================================================================

USE my_guitar_shop;

SELECT c.category_name, p.product_name, p.list_price
FROM categories c
    INNER JOIN products p
        ON c.category_id = p.category_id
ORDER BY c.category_name ASC, p.product_name ASC;
