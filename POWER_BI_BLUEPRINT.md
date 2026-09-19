# Power BI Report Blueprint

## Objective

Build a recruiter-ready three-page Power BI report from `customers.csv` and `transactions.csv`.

## Data Model

Create a one-to-many relationship:

```text
Customers[customer_id]  1 ───── *  Transactions[customer_id]
```

Create a dedicated Date table:

```DAX
Date =
ADDCOLUMNS(
    CALENDAR(
        MIN(Transactions[transaction_date]),
        MAX(Transactions[transaction_date])
    ),
    "Year", YEAR([Date]),
    "Month Number", MONTH([Date]),
    "Month", FORMAT([Date], "MMM"),
    "Year Month", FORMAT([Date], "YYYY-MM")
)
```

Relate:

```text
Date[Date]  1 ───── *  Transactions[transaction_date]
```

Mark `Date` as the Power BI date table.

---

## Page 1 — Executive Overview

### KPI Cards

- Total Customers
- Total Spend
- Total Transactions
- Average Transaction Value
- Average Credit Limit
- Average Utilization %

### Visuals

1. **Line chart** — Total Spend by Year Month
2. **Column chart** — Total Spend by Card Type
3. **Bar chart** — Total Spend by Transaction Category
4. **Donut chart** — Total Spend by Channel
5. **Slicers** — Card Type, Gender, Customer Value Segment, Churn Risk Segment

### Purpose

Give a hiring manager or business stakeholder the portfolio summary in under 30 seconds.

---

## Page 2 — Customer Analytics

### KPI Cards

- Spend Per Customer
- High Value Customers
- Active Customers
- Inactive Customers

### Visuals

1. **Bar chart** — Customers by Customer Value Segment
2. **Column chart** — Spend by Customer Value Segment
3. **Scatter plot** — Annual Income vs Credit Limit, sized by customer spend
4. **Bar chart** — Customers by Age Band
5. **Table** — Top 10 Customers with card type, spend, value segment, and risk segment

### Suggested Age Band

```DAX
Age Band =
SWITCH(
    TRUE(),
    Customers[age] < 30, "21-29",
    Customers[age] < 40, "30-39",
    Customers[age] < 50, "40-49",
    Customers[age] < 60, "50-59",
    "60+"
)
```

---

## Page 3 — Risk & Engagement

### KPI Cards

- High Risk Customers
- Average Utilization %
- High Utilization Customers
- Inactive Customers

### Visuals

1. **Donut chart** — Customers by Churn Risk Segment
2. **Donut chart** — Active vs Inactive
3. **Bar chart** — Risk Segment by Customer Value Segment
4. **Table** — High-utilization customers
5. **Matrix** — Customer Value Segment × Risk Segment

### Suggested High Utilization Measure

```DAX
High Utilization Customers =
CALCULATE(
    DISTINCTCOUNT(Customers[customer_id]),
    Customers[utilization_ratio] >= 0.70
)
```

---

## Visual Design Guidance

Use a restrained professional style:

- Dark navy or clean white background
- One primary accent color
- Consistent KPI-card sizing
- Maximum 5–6 visuals per page
- Use whitespace between sections
- Avoid decorative charts that do not answer a business question
- Keep chart titles descriptive, e.g. **Monthly Transaction Value** instead of **Trend**

## Interaction Design

- Sync key slicers across pages.
- Allow cross-filtering between card, category, channel, and customer visuals.
- Add a Reset Filters bookmark.
- Add tooltip pages for customer and card-type details if desired.

## Interview Talking Points

Be prepared to explain:

- Why you separated customer and transaction tables.
- Why a Date table is required for time intelligence.
- Difference between calculated columns and measures.
- Why `DIVIDE()` is preferable to direct division in DAX.
- How filter context affects measures.
- How you would extend the model with payments, delinquency, or profitability data.
