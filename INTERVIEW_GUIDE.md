# Interview Guide — Credit Card Customer Analytics

## 30-Second Project Explanation

“I built an end-to-end credit-card customer analytics project using Python, SQL, Streamlit, and Power BI-ready DAX. I generated a reproducible synthetic dataset with 2,500 customers and 40,000 transactions, modeled customer-to-transaction relationships, wrote SQL for KPI and window-function analysis, created customer value and risk segments, and built an interactive dashboard. I also added automated GitHub Actions tests so the project can be reproduced reliably.”

## Common Interview Questions

### Why did you choose this project?

It demonstrates both technical analytics skills and business thinking: customer segmentation, transaction trends, utilization, channel analysis, and actionable recommendations.

### Why use two tables?

Customer attributes belong at customer grain, while transactions occur many times per customer. Separating them avoids repeating customer data and creates a clean one-to-many model.

### What is the grain of each table?

- Customers: one row per customer.
- Transactions: one row per transaction.

### What advanced SQL did you use?

CTEs, `LAG()`, `DENSE_RANK()`, `NTILE()`, running totals, partitioned ranking, contribution analysis, and recency calculations.

### How did you define High Value customers?

The project uses spend distribution. The top 15% of customers by annual spend are labeled High Value. The threshold is derived from the generated dataset rather than hard-coded currency values.

### Is churn risk predicted by machine learning?

No. It is a rule-based analytical segment used to demonstrate portfolio segmentation. A production churn model would require labeled historical churn outcomes and proper model validation.

### What would you add with real banking data?

Payment history, delinquency, interest revenue, fees, rewards cost, profitability, product holdings, true churn outcomes, acquisition channel, geography, and customer-service interactions.

### Why do you need a Date table in Power BI?

A dedicated Date dimension provides consistent filtering and is required for reliable time-intelligence patterns such as previous month, year-over-year, and year-to-date calculations.

### What was the most important insight?

The useful insight is not just the largest category or channel; it is the intersection of **customer value and engagement/risk**. High-value customers with risk flags should be analyzed separately because losing engagement from a valuable segment has greater business impact.

### What is one limitation?

The data is synthetic, so the project demonstrates analytical workflow and decision framing rather than conclusions about a real bank or real customers.

## SQL Questions to Practice

1. Find the top 10 customers by spend.
2. Calculate month-over-month growth.
3. Rank customers within each card type.
4. Calculate each category’s percentage contribution.
5. Find customers whose utilization exceeds 70%.
6. Calculate a running total of monthly spend.
7. Create spend quartiles with `NTILE()`.
8. Find each customer’s latest transaction date.

## Power BI Questions to Practice

1. Measure vs calculated column?
2. Row context vs filter context?
3. Why use `DIVIDE()`?
4. How does `CALCULATE()` change filter context?
5. How would you calculate MoM growth?
6. Why build a star-style model?
7. Why avoid putting everything in one flat table?

## Final Interview Rule

Do not only describe the charts. Explain:

**business question → analysis method → finding → possible action → limitation**
