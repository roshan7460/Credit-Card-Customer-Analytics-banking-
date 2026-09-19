DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    age INTEGER,
    gender TEXT,
    annual_income REAL,
    education TEXT,
    marital_status TEXT,
    card_type TEXT,
    credit_limit REAL,
    tenure_years INTEGER,
    customer_status TEXT,
    outstanding_balance REAL,
    utilization_ratio REAL,
    churn_risk_segment TEXT,
    customer_value_segment TEXT
);

CREATE TABLE transactions (
    transaction_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    transaction_date DATE,
    transaction_category TEXT,
    merchant TEXT,
    channel TEXT,
    transaction_amount REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
