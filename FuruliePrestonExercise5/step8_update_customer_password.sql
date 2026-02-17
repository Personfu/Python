-- =============================================================================
-- MySQL Exercise 5 - Step 8
-- Author: Preston Furulie
-- Database: my_guitar_shop
-- Description: UPDATE the Customers table to change the password column
--              to 'secret' for the customer with email rick@raven.com.
-- =============================================================================

USE my_guitar_shop;

-- Update the password for rick@raven.com
UPDATE customers
SET password = 'secret'
WHERE email_address = 'rick@raven.com';

-- Verify the update was successful
SELECT customer_id, email_address, password, first_name, last_name
FROM customers
WHERE email_address = 'rick@raven.com';
