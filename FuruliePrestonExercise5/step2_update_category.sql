-- =============================================================================
-- MySQL Exercise 5 - Step 2
-- Author: Preston Furulie
-- Database: my_guitar_shop
-- Description: UPDATE the row added in Step 1 to change the category_name
--              from 'Brass' to 'Woodwinds'. Uses the category_id column
--              to identify the specific row.
-- =============================================================================

USE my_guitar_shop;

-- Update the category name from 'Brass' to 'Woodwinds'
-- The category_id value (5) was auto-generated in Step 1
UPDATE categories
SET category_name = 'Woodwinds'
WHERE category_id = 5;

-- Verify the update was successful
SELECT *
FROM categories;
