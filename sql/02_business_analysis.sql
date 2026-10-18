
-- Business question:
-- What proportion of customers are labelled as churned?

SELECT
    COUNT(*) AS total_customers,
    SUM(
        CASE
            WHEN churn = 'Yes' THEN 1
            ELSE 0
        END
    ) AS churned_customers,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN churn = 'Yes' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS observed_churn_percentage
FROM public.telco_customers;



-- Business question:
-- What is the observed churn percentage for each contract type?

SELECT
    contract,
    COUNT(*) AS total_customers,
    SUM(
        CASE
            WHEN churn = 'Yes' THEN 1
            ELSE 0
        END
    ) AS churned_customers,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN churn = 'Yes' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS observed_churn_percentage
FROM public.telco_customers
GROUP BY contract
ORDER BY observed_churn_percentage DESC;


-- Business Question 2:
-- Is customer churn associated with payment method?

SELECT
    payment_method,
    COUNT(*) AS total_customers,
    SUM(
        CASE
            WHEN churn = 'Yes' THEN 1
            ELSE 0
        END
    ) AS churned_customers,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN churn = 'Yes' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS observed_churn_percentage
FROM public.telco_customers
GROUP BY payment_method
ORDER BY observed_churn_percentage DESC;


-- Business Question 3:
-- How does observed churn vary by customer tenure?

SELECT
    CASE
        WHEN tenure <= 12 THEN 'New (0-12 months)'
        WHEN tenure <= 48 THEN 'Medium (13-48 months)'
        ELSE 'Long (49-72 months)'
    END AS tenure_group,
    COUNT(*) AS total_customers,
    SUM(
        CASE
            WHEN churn = 'Yes' THEN 1
            ELSE 0
        END
    ) AS churned_customers,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN churn = 'Yes' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS observed_churn_percentage
FROM public.telco_customers
GROUP BY
    CASE
        WHEN tenure <= 12 THEN 'New (0-12 months)'
        WHEN tenure <= 48 THEN 'Medium (13-48 months)'
        ELSE 'Long (49-72 months)'
    END
ORDER BY MIN(tenure);
