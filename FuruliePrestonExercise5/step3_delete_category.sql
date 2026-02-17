-- =============================================================================
-- MySQL Exercise 5 - Step 3
-- Author: Preston Furulie
-- Database: my_guitar_shop
-- Description: DELETE the row added in Step 1 from the Categories table.
--              Uses the category_id column to identify the row to delete.
-- =============================================================================

USE my_guitar_shop;

-- Delete the category that was added in Step 1
DELETE FROM categories
WHERE category_id = 5;

-- Verify the delete was successful
SELECT *
FROM categories;
