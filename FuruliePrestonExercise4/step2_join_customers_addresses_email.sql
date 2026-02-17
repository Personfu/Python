-- =============================================================================
-- MySQL Exercise 4 - Step 2
-- Author: Preston Furulie
-- Database: my_guitar_shop
-- Description: JOIN the Customers table to the Addresses table.
--              Returns first_name, last_name, line1, city, state, zip_code.
--              Filtered to return only rows for the customer with the
--              email address allan.sherwood@yahoo.com.
-- =============================================================================

USE my_guitar_shop;

SELECT c.first_name, c.last_name, a.line1, a.city, a.state, a.zip_code
FROM customers c
    INNER JOIN addresses a
        ON c.customer_id = a.customer_id
WHERE c.email_address = 'allan.sherwood@yahoo.com';
