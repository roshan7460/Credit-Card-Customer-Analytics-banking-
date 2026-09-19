from pathlib import Path
import numpy as np
import pandas as pd


def generate_data(n_customers: int = 2500, n_transactions: int = 40000, seed: int = 42):
    """Generate deterministic synthetic credit-card customer and transaction data."""
    rng = np.random.default_rng(seed)
    customer_ids = np.array([f"CUST{i:05d}" for i in range(1, n_customers + 1)])

    genders = rng.choice(["Male", "Female"], size=n_customers, p=[0.53, 0.47])
    ages = np.clip(rng.normal(41, 11, size=n_customers).round().astype(int), 21, 70)
    income = np.clip(rng.lognormal(mean=11.0, sigma=0.45, size=n_customers), 25000, 300000).round().astype(int)
    education = rng.choice(
        ["Graduate", "Post-Graduate", "High School", "Doctorate"],
        size=n_customers,
        p=[0.48, 0.28, 0.18, 0.06],
    )
    marital = rng.choice(["Single", "Married", "Divorced"], size=n_customers, p=[0.36, 0.54, 0.10])

    card_types = []
    for inc in income:
        if inc > 180000:
            card_types.append(rng.choice(["Platinum", "Gold"], p=[0.75, 0.25]))
        elif inc > 100000:
            card_types.append(rng.choice(["Gold", "Platinum", "Silver"], p=[0.60, 0.15, 0.25]))
        elif inc > 60000:
            card_types.append(rng.choice(["Silver", "Gold"], p=[0.78, 0.22]))
        else:
            card_types.append(rng.choice(["Classic", "Silver"], p=[0.75, 0.25]))
    card_types = np.array(card_types)

    limit_mult = {"Classic": 0.35, "Silver": 0.50, "Gold": 0.75, "Platinum": 1.05}
    credit_limit = np.array([
        income[i] * limit_mult[card_types[i]] * rng.uniform(0.7, 1.3)
        for i in range(n_customers)
    ])
    credit_limit = np.clip(credit_limit, 20000, 250000).round().astype(int)

    customers = pd.DataFrame({
        "customer_id": customer_ids,
        "age": ages,
        "gender": genders,
        "annual_income": income,
        "education": education,
        "marital_status": marital,
        "card_type": card_types,
        "credit_limit": credit_limit,
        "tenure_years": rng.integers(1, 13, size=n_customers),
        "customer_status": rng.choice(["Active", "Inactive"], size=n_customers, p=[0.86, 0.14]),
    })

    customer_idx = rng.choice(np.arange(n_customers), size=n_transactions, replace=True)
    start = np.datetime64("2025-01-01")
    txn_dates = start + rng.integers(0, 365, size=n_transactions).astype("timedelta64[D]")
    categories = np.array([
        "Groceries", "Travel", "Dining", "Shopping",
        "Utilities", "Fuel", "Entertainment", "Healthcare"
    ])
    cat_probs = np.array([0.19, 0.10, 0.16, 0.20, 0.11, 0.10, 0.08, 0.06])
    txn_categories = rng.choice(categories, size=n_transactions, p=cat_probs)
    base_amount = {
        "Groceries": 70, "Travel": 220, "Dining": 90, "Shopping": 140,
        "Utilities": 110, "Fuel": 75, "Entertainment": 80, "Healthcare": 130
    }

    amounts = np.empty(n_transactions)
    median_income = np.median(income)
    card_factor = {"Classic": 0.85, "Silver": 1.0, "Gold": 1.25, "Platinum": 1.55}

    for i in range(n_transactions):
        ci = customer_idx[i]
        income_factor = income[ci] / median_income
        amounts[i] = max(
            5,
            rng.gamma(2.2, base_amount[txn_categories[i]] / 2.2)
            * (0.65 + 0.35 * income_factor)
            * card_factor[card_types[ci]],
        )

    transactions = pd.DataFrame({
        "transaction_id": [f"TXN{i:07d}" for i in range(1, n_transactions + 1)],
        "customer_id": customer_ids[customer_idx],
        "transaction_date": pd.to_datetime(txn_dates),
        "transaction_category": txn_categories,
        "merchant": rng.choice(
            ["Amazon", "Flipkart", "Reliance", "DMart", "MakeMyTrip",
             "Swiggy", "Zomato", "IndianOil", "Apollo", "BookMyShow"],
            size=n_transactions,
        ),
        "channel": rng.choice(["Online", "POS", "Contactless"], size=n_transactions, p=[0.47, 0.38, 0.15]),
        "transaction_amount": np.round(amounts, 2),
    })

    annual_spend = (
        transactions.groupby("customer_id")["transaction_amount"]
        .sum()
        .reindex(customer_ids)
        .fillna(0)
        .to_numpy()
    )

    utilization = np.clip(
        (annual_spend / 12) / np.maximum(credit_limit, 1) + rng.normal(0.15, 0.08, n_customers),
        0.03,
        0.95,
    )
    customers["outstanding_balance"] = np.round(credit_limit * utilization).astype(int)
    customers["utilization_ratio"] = np.round(
        customers["outstanding_balance"] / customers["credit_limit"], 4
    )

    customers["churn_risk_segment"] = np.where(
        (customers["customer_status"] == "Inactive")
        | (customers["utilization_ratio"] > 0.75)
        | ((customers["tenure_years"] <= 2) & (customers["utilization_ratio"] < 0.10)),
        "High",
        np.where(
            (customers["utilization_ratio"] > 0.55) | (customers["tenure_years"] <= 3),
            "Medium",
            "Low",
        ),
    )

    spend_series = pd.Series(annual_spend, index=customers.index)
    q20, q50, q85 = spend_series.quantile([0.20, 0.50, 0.85])
    customers["customer_value_segment"] = np.select(
        [spend_series >= q85, spend_series >= q50, spend_series >= q20],
        ["High Value", "Growth", "Core"],
        default="Low Engagement",
    )

    return customers, transactions


def ensure_csvs(directory: Path):
    directory = Path(directory)
    customers_path = directory / "customers.csv"
    transactions_path = directory / "transactions.csv"

    if customers_path.exists() and transactions_path.exists():
        customers = pd.read_csv(customers_path)
        transactions = pd.read_csv(transactions_path, parse_dates=["transaction_date"])
        if "customer_value_segment" in customers.columns:
            return customers, transactions

    customers, transactions = generate_data()
    customers.to_csv(customers_path, index=False)
    transactions.to_csv(transactions_path, index=False)
    return customers, transactions


if __name__ == "__main__":
    base = Path(__file__).resolve().parent
    c, t = ensure_csvs(base)
    print(f"Generated {len(c):,} customers and {len(t):,} transactions in {base}")
