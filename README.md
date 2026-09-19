# 💳 Credit Card Customer & Transaction Analytics

End-to-end **Data Analyst portfolio project** using **SQL, Python, Streamlit, Power BI-ready modeling and DAX**.

[![CI](https://github.com/roshan7460/Credit-Card-Customer-Analytics-banking-/actions/workflows/ci.yml/badge.svg)](https://github.com/roshan7460/Credit-Card-Customer-Analytics-banking-/actions/workflows/ci.yml)

## 🔗 Live dashboard preview

**[Open the browser dashboard](https://htmlpreview.github.io/?https://github.com/roshan7460/Credit-Card-Customer-Analytics-banking-/blob/main/index.html)**

The repository also contains the full Streamlit application. Clone it and run `streamlit run app.py` for interactive filters and customer-level analytics.

## 🎯 Business objective

Analyze customer behavior, credit-card transaction trends, card usage, credit utilization, customer value and churn-risk segments to support portfolio and customer-engagement decisions.

## ✅ Included

- Deterministic synthetic data generator: **2,500 customers + 40,000 transactions**
- Interactive Streamlit dashboard
- SQL schema and 10 analytical SQL queries
- SQLite database builder
- Power BI-ready relationship and DAX measures
- Browser-based dashboard preview
- GitHub Actions CI smoke test

## 🧱 Project structure

```text
.
├── app.py
├── data_generator.py
├── build_database.py
├── schema.sql
├── analysis.sql
├── powerbi_dax_measures.txt
├── requirements.txt
├── index.html
├── .gitignore
└── .github/workflows/ci.yml
```

`customers.csv`, `transactions.csv`, and `credit_card_analytics.db` are generated locally and excluded from Git because they are reproducible.

## ▶️ Run locally

```bash
git clone https://github.com/roshan7460/Credit-Card-Customer-Analytics-banking-.git
cd Credit-Card-Customer-Analytics-banking-
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install and run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app automatically generates the dataset on first run and normally opens at `http://localhost:8501`.

## 🗄️ Build SQLite

```bash
python build_database.py
```

This creates `credit_card_analytics.db`. Open it in DB Browser for SQLite, DBeaver, or VS Code and run queries from `analysis.sql`.

## 📊 Dashboard KPIs

Total Customers • Total Spend • Total Transactions • Average Transaction Value • Average Credit Limit • Average Credit Utilization • Monthly Spend Trend • Spend by Category • Spend by Channel • Card-Type Distribution • Top 10 Customers • Churn-Risk Segmentation

## 🧮 Power BI model

Generate CSV files:

```bash
python data_generator.py
```

Import `customers.csv` and `transactions.csv` and create:

```text
Customers[customer_id]  1 ───── *  Transactions[customer_id]
```

Use the measures in `powerbi_dax_measures.txt`.

Recommended pages:
1. **Executive Overview**
2. **Customer Analytics**
3. **Risk & Transaction Analysis**

## 🧠 SQL analysis

`analysis.sql` includes overall KPIs, card-type performance, monthly trends, top customers, category analysis, high-utilization customers, churn-risk segmentation, channel performance and customer-value bands.

## 📌 Portfolio note

The dataset is synthetic and reproducible with a fixed random seed. The churn-risk field is a **rule-based analytical segmentation**, not a production machine-learning prediction model.

## 📄 Resume-ready description

**Credit Card Customer & Transaction Analytics | SQL, Power BI, DAX, Python**

- Built an end-to-end analytics project using 40K synthetic transaction records and 2.5K customer records.
- Developed SQL queries for KPI analysis, customer segmentation, monthly trends, high-value customers and credit utilization.
- Built an interactive Streamlit dashboard with filters for card type, gender, churn risk and transaction date.
- Created Power BI-ready data modeling and DAX measures for spend, transaction value, utilization and growth analysis.
