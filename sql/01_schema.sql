
-- Customer Churn Analysis
-- File: 01_schema.sql
-- Purpose: Document the structure of the customer table.
-- Existing table: public.telco_customers
-- Verified row count: 7043

-- Inspect the existing table structure.
-- This does not create or modify the table.
\d+ public.telco_customers

-- Verify the number of customer records.
SELECT COUNT(*) AS total_customers
FROM public.telco_customers;

-- Verify the churn categories and counts.
SELECT
    churn,
    COUNT(*) AS customer_count
FROM public.telco_customers
GROUP BY churn
ORDER BY churn;
