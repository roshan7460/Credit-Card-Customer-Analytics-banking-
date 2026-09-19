-- ADVANCED PORTFOLIO SQL
-- SQLite-compatible examples demonstrating CTEs and window functions.

-- 1. Month-over-month transaction value growth
WITH monthly AS (
    SELECT
        strftime('%Y-%m', transaction_date) AS month,
        SUM(transaction_amount) AS total_spend
    FROM transactions
    GROUP BY strftime('%Y-%m', transaction_date)
),
with_previous AS (
    SELECT
        month,
        total_spend,
        LAG(total_spend) OVER (ORDER BY month) AS previous_month_spend
    FROM monthly
)
SELECT
    month,
    ROUND(total_spend, 2) AS total_spend,
    ROUND(previous_month_spend, 2) AS previous_month_spend,
    ROUND(
        (total_spend - previous_month_spend) * 100.0
        / NULLIF(previous_month_spend, 0),
        2
    ) AS mom_growth_pct
FROM with_previous
ORDER BY month;


-- 2. Running transaction value through the year
WITH monthly AS (
    SELECT
        strftime('%Y-%m', transaction_date) AS month,
        SUM(transaction_amount) AS total_spend
    FROM transactions
    GROUP BY strftime('%Y-%m', transaction_date)
)
SELECT
    month,
    ROUND(total_spend, 2) AS monthly_spend,
    ROUND(
        SUM(total_spend) OVER (
            ORDER BY month
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ),
        2
    ) AS running_spend
FROM monthly
ORDER BY month;


-- 3. Rank customers by annual spend
WITH customer_spend AS (
    SELECT
        customer_id,
        SUM(transaction_amount) AS total_spend,
        COUNT(*) AS transaction_count
    FROM transactions
    GROUP BY customer_id
)
SELECT
    customer_id,
    ROUND(total_spend, 2) AS total_spend,
    transaction_count,
    DENSE_RANK() OVER (ORDER BY total_spend DESC) AS spend_rank
FROM customer_spend
ORDER BY spend_rank
LIMIT 25;


-- 4. Rank customers within each card type
WITH customer_spend AS (
    SELECT
        c.customer_id,
        c.card_type,
        SUM(t.transaction_amount) AS total_spend
    FROM customers c
    JOIN transactions t
        ON t.customer_id = c.customer_id
    GROUP BY c.customer_id, c.card_type
)
SELECT
    customer_id,
    card_type,
    ROUND(total_spend, 2) AS total_spend,
    DENSE_RANK() OVER (
        PARTITION BY card_type
        ORDER BY total_spend DESC
    ) AS rank_within_card
FROM customer_spend
ORDER BY card_type, rank_within_card;


-- 5. Category contribution to total transaction value
WITH category_spend AS (
    SELECT
        transaction_category,
        SUM(transaction_amount) AS total_spend
    FROM transactions
    GROUP BY transaction_category
)
SELECT
    transaction_category,
    ROUND(total_spend, 2) AS total_spend,
    ROUND(
        total_spend * 100.0 / SUM(total_spend) OVER (),
        2
    ) AS portfolio_share_pct
FROM category_spend
ORDER BY total_spend DESC;


-- 6. Merchant ranking inside each transaction category
WITH merchant_spend AS (
    SELECT
        transaction_category,
        merchant,
        SUM(transaction_amount) AS total_spend
    FROM transactions
    GROUP BY transaction_category, merchant
)
SELECT
    transaction_category,
    merchant,
    ROUND(total_spend, 2) AS total_spend,
    DENSE_RANK() OVER (
        PARTITION BY transaction_category
        ORDER BY total_spend DESC
    ) AS merchant_rank
FROM merchant_spend
ORDER BY transaction_category, merchant_rank;


-- 7. Customer value quartiles using NTILE
WITH customer_spend AS (
    SELECT
        customer_id,
        SUM(transaction_amount) AS total_spend
    FROM transactions
    GROUP BY customer_id
),
ranked AS (
    SELECT
        customer_id,
        total_spend,
        NTILE(4) OVER (ORDER BY total_spend DESC) AS spend_quartile
    FROM customer_spend
)
SELECT
    spend_quartile,
    COUNT(*) AS customers,
    ROUND(AVG(total_spend), 2) AS avg_customer_spend,
    ROUND(MIN(total_spend), 2) AS min_customer_spend,
    ROUND(MAX(total_spend), 2) AS max_customer_spend
FROM ranked
GROUP BY spend_quartile
ORDER BY spend_quartile;


-- 8. Customer value segment performance
SELECT
    c.customer_value_segment,
    COUNT(DISTINCT c.customer_id) AS customers,
    COUNT(t.transaction_id) AS transactions,
    ROUND(SUM(t.transaction_amount), 2) AS total_spend,
    ROUND(
        SUM(t.transaction_amount) / COUNT(DISTINCT c.customer_id),
        2
    ) AS spend_per_customer
FROM customers c
JOIN transactions t
    ON t.customer_id = c.customer_id
GROUP BY c.customer_value_segment
ORDER BY total_spend DESC;


-- 9. High-value customers with risk or utilization attention flags
WITH customer_spend AS (
    SELECT
        customer_id,
        SUM(transaction_amount) AS total_spend
    FROM transactions
    GROUP BY customer_id
)
SELECT
    c.customer_id,
    c.card_type,
    c.customer_value_segment,
    c.churn_risk_segment,
    ROUND(c.utilization_ratio * 100, 2) AS utilization_pct,
    ROUND(s.total_spend, 2) AS annual_spend,
    CASE
        WHEN c.customer_value_segment = 'High Value'
             AND c.churn_risk_segment = 'High'
            THEN 'Retention Priority'
        WHEN c.customer_value_segment = 'High Value'
             AND c.utilization_ratio >= 0.70
            THEN 'Monitor Utilization'
        WHEN c.customer_value_segment = 'High Value'
            THEN 'Premium Engagement'
        ELSE 'Standard'
    END AS recommended_action_segment
FROM customers c
JOIN customer_spend s
    ON s.customer_id = c.customer_id
WHERE c.customer_value_segment = 'High Value'
ORDER BY annual_spend DESC;


-- 10. Latest activity date and recency by customer
WITH latest_date AS (
    SELECT MAX(transaction_date) AS dataset_max_date
    FROM transactions
),
customer_activity AS (
    SELECT
        customer_id,
        MAX(transaction_date) AS last_transaction_date,
        COUNT(*) AS transaction_count,
        SUM(transaction_amount) AS total_spend
    FROM transactions
    GROUP BY customer_id
)
SELECT
    a.customer_id,
    a.last_transaction_date,
    CAST(
        julianday(d.dataset_max_date) - julianday(a.last_transaction_date)
        AS INTEGER
    ) AS days_since_last_transaction,
    a.transaction_count,
    ROUND(a.total_spend, 2) AS total_spend
FROM customer_activity a
CROSS JOIN latest_date d
ORDER BY days_since_last_transaction DESC, total_spend DESC;
