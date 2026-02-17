-- =============================================================================
-- MySQL Exercise 4 - Step 6
-- Author: Preston Furulie
-- Database: my_guitar_shop
-- Description: LEFT OUTER JOIN the Categories table to the Products table
--              to find categories that have never been used (i.e., no
--              products assigned). Returns category_name and product_id.
--              Filters for rows where product_id IS NULL, indicating
--              no matching product exists for that category.
-- =============================================================================

USE my_guitar_shop;

SELECT c.category_name, p.product_id
FROM categories c
    LEFT JOIN products p
        ON c.category_id = p.category_id
WHERE p.product_id IS NULL;
