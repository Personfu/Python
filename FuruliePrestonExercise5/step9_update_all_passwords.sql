-- =============================================================================
-- MySQL Exercise 5 - Step 9
-- Author: Preston Furulie
-- Database: my_guitar_shop
-- Description: UPDATE the Customers table to change the password column
--              to 'reset' for every customer. Uses a LIMIT clause to
--              avoid safe-update mode errors.
-- =============================================================================

USE my_guitar_shop;

-- Update the password to 'reset' for all customers in the table
-- LIMIT 100 is included to handle MySQL safe-update mode
UPDATE customers
SET password = 'reset'
LIMIT 100;

-- Verify the update was successful
SELECT customer_id, email_address, password, first_name, last_name
FROM customers;
