-- =============================================================================
-- MySQL Exercise 4 - Step 5
-- Author: Preston Furulie
-- Database: my_guitar_shop
-- Description: Self-join on the Products table to find products that share
--              the same list_price as another product.
--              Uses a self-join where product_id values differ but
--              list_price values match.
--              Returns product_name and list_price, sorted by product_name.
-- =============================================================================

USE my_guitar_shop;

SELECT DISTINCT p1.product_name, p1.list_price
FROM products p1
    INNER JOIN products p2
        ON p1.product_id != p2.product_id
        AND p1.list_price = p2.list_price
ORDER BY p1.product_name ASC;
