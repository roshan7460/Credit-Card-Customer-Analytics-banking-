-- 1. Overall KPIs
SELECT
    COUNT(DISTINCT customer_id) AS total_customers,
    ROUND(AVG(credit_limit), 2) AS avg_credit_limit,
    ROUND(AVG(utilization_ratio) * 100, 2) AS avg_utilization_pct
FROM customers;

-- 2. Total transaction value and count
SELECT
    ROUND(SUM(transaction_amount), 2) AS total_spend,
    COUNT(*) AS total_transactions,
    ROUND(AVG(transaction_amount), 2) AS avg_transaction_value
FROM transactions;

-- 3. Spend by card type
SELECT
    c.card_type,
    COUNT(DISTINCT c.customer_id) AS customers,
    COUNT(t.transaction_id) AS transactions,
    ROUND(SUM(t.transaction_amount), 2) AS total_spend,
    ROUND(AVG(t.transaction_amount), 2) AS avg_transaction_value
FROM customers c
JOIN transactions t ON c.customer_id = t.customer_id
GROUP BY c.card_type
ORDER BY total_spend DESC;

-- 4. Monthly trend
SELECT
    strftime('%Y-%m', transaction_date) AS month,
    ROUND(SUM(transaction_amount), 2) AS total_spend,
    COUNT(*) AS transactions
FROM transactions
GROUP BY strftime('%Y-%m', transaction_date)
ORDER BY month;

-- 5. Top 10 customers by spend
SELECT
    t.customer_id,
    c.card_type,
    c.annual_income,
    ROUND(SUM(t.transaction_amount), 2) AS total_spend
FROM transactions t
JOIN customers c ON c.customer_id = t.customer_id
GROUP BY t.customer_id, c.card_type, c.annual_income
ORDER BY total_spend DESC
LIMIT 10;

-- 6. Spend by category
SELECT
    transaction_category,
    ROUND(SUM(transaction_amount), 2) AS total_spend,
    COUNT(*) AS transactions,
    ROUND(AVG(transaction_amount), 2) AS avg_transaction_value
FROM transactions
GROUP BY transaction_category
ORDER BY total_spend DESC;

-- 7. High utilization customers
SELECT
    customer_id,
    card_type,
    credit_limit,
    outstanding_balance,
    ROUND(utilization_ratio * 100, 2) AS utilization_pct
FROM customers
WHERE utilization_ratio >= 0.70
ORDER BY utilization_ratio DESC;

-- 8. Churn-risk segmentation
SELECT
    churn_risk_segment,
    COUNT(*) AS customers,
    ROUND(AVG(utilization_ratio) * 100, 2) AS avg_utilization_pct,
    ROUND(AVG(annual_income), 2) AS avg_income
FROM customers
GROUP BY churn_risk_segment
ORDER BY CASE churn_risk_segment
    WHEN 'High' THEN 1
    WHEN 'Medium' THEN 2
    ELSE 3
END;

-- 9. Channel performance
SELECT
    channel,
    COUNT(*) AS transactions,
    ROUND(SUM(transaction_amount), 2) AS total_spend,
    ROUND(AVG(transaction_amount), 2) AS avg_transaction_value
FROM transactions
GROUP BY channel
ORDER BY total_spend DESC;

-- 10. Customer value bands
WITH customer_spend AS (
    SELECT customer_id, SUM(transaction_amount) AS total_spend
    FROM transactions
    GROUP BY customer_id
)
SELECT
    CASE
        WHEN total_spend >= 5000 THEN 'High Value'
        WHEN total_spend >= 2500 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS customer_value_segment,
    COUNT(*) AS customers,
    ROUND(AVG(total_spend), 2) AS avg_annual_spend
FROM customer_spend
GROUP BY customer_value_segment
ORDER BY avg_annual_spend DESC;
