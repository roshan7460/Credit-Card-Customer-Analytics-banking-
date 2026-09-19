# Credit Card Customer Analytics — Case Study

## 1. Business Context

A retail bank wants a clearer view of credit-card customer behavior. The analysis should help teams understand portfolio activity, customer value, credit utilization, engagement risk, and transaction-channel patterns.

The project is designed as a realistic **Data Analyst portfolio case study** rather than a production lending model.

## 2. Analytical Questions

The project focuses on six practical business questions:

1. Which customers and card types generate the most transaction value?
2. Which categories and channels drive portfolio activity?
3. How does transaction value change month over month?
4. Which customers appear highly engaged or low-engagement?
5. Which high-value customers also show risk or utilization flags?
6. What actions could a customer-engagement team consider by segment?

## 3. Data

The synthetic dataset contains:

- **2,500 customers**
- **40,000 transactions**
- Customer demographics and income
- Card type and credit limit
- Outstanding balance and utilization
- Transaction category, merchant, channel, date, and amount
- Rule-based risk segment
- Spend-based customer value segment

The generator uses a fixed random seed so results are reproducible.

## 4. Data Model

The model uses a simple one-to-many structure:

```text
Customers[customer_id]  1 ───── *  Transactions[customer_id]
```

This supports both SQL analysis and Power BI / Streamlit reporting.

## 5. Analysis Approach

### Python

Python is used to create reproducible synthetic data and derive analytical features.

### SQL

SQL covers:

- KPI aggregation
- Monthly trends
- Customer ranking
- Category contribution
- Channel performance
- High-utilization customers
- Window functions
- Running totals
- Month-over-month growth
- Customer ranking within card type
- Recency analysis

### Dashboard

The Streamlit dashboard is organized into:

- Executive Overview
- Customer Segmentation
- Risk & Engagement

### Power BI / DAX

The project includes a Power BI-ready data model and reusable DAX measures for KPI cards, time intelligence, segmentation, and growth.

## 6. Customer Segmentation

### Customer Value Segment

Customers are segmented using annual spend distribution:

- **High Value** — top 15%
- **Growth** — next 35%
- **Core** — next 30%
- **Low Engagement** — bottom 20%

This segmentation is useful for portfolio analysis and campaign design.

### Churn-Risk Segment

The risk segment is intentionally rule-based and uses customer status, utilization, and tenure. It is included to demonstrate analytical segmentation and should not be interpreted as a production predictive model.

## 7. Key Portfolio Findings

The deterministic portfolio demonstrates several patterns:

- Shopping is the largest transaction category by transaction value.
- Online is the largest transaction channel.
- Silver is the largest card-type customer segment.
- A subset of customers combines high value with risk or utilization flags.
- Monthly activity is relatively stable, which makes changes in month-over-month performance easy to identify.
- High-value segmentation creates a clear target group for premium engagement analysis.

## 8. Business Recommendations

These are analytical recommendations for a fictional portfolio:

### Retention Priority

Review **High Value + High Risk** customers separately. Their value means disengagement could have a disproportionate impact on portfolio activity.

### Premium Engagement

Use High Value customers with healthy engagement as a target group for premium offers, loyalty benefits, or cross-sell analysis.

### Low Engagement

For Low Engagement customers, analyze recency and transaction count before designing reactivation campaigns.

### Channel Strategy

Because Online is the largest channel, digital offers and personalized online experiences can be evaluated first when testing engagement campaigns.

### Category Partnerships

High-spend categories can be used to identify potential merchant partnerships, reward categories, or targeted promotions.

### Utilization Monitoring

High utilization should be monitored as a portfolio indicator. It should not, by itself, be interpreted as credit risk or customer quality.

## 9. Limitations

- The dataset is synthetic.
- The portfolio covers a single generated year.
- The risk segment is rule-based.
- There is no profitability, delinquency, payment history, or actual churn outcome.
- No causal claims should be made from the descriptive analysis.

## 10. What This Project Demonstrates

This project demonstrates the skills expected in an entry-level or junior Data Analyst role:

- SQL querying
- Window functions and CTEs
- Data modeling
- KPI design
- Dashboard design
- Power BI / DAX concepts
- Python data preparation
- Business interpretation
- GitHub documentation
- Automated testing
