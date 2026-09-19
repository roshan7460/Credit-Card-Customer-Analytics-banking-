import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from data_generator import ensure_csvs

st.set_page_config(page_title="Credit Card Customer Analytics", page_icon="💳", layout="wide")
BASE = Path(__file__).parent

@st.cache_data
def load_data():
    return ensure_csvs(BASE)

customers, tx = load_data()

st.title("💳 Credit Card Customer & Transaction Analytics")
st.caption("Portfolio project | SQL • Power BI • DAX • Python • Streamlit")

st.sidebar.header("Filters")
card_types = ["All"] + sorted(customers["card_type"].dropna().unique().tolist())
selected_card = st.sidebar.selectbox("Card Type", card_types)
genders = ["All"] + sorted(customers["gender"].dropna().unique().tolist())
selected_gender = st.sidebar.selectbox("Gender", genders)
risk_levels = ["All", "Low", "Medium", "High"]
selected_risk = st.sidebar.selectbox("Churn Risk", risk_levels)

min_date = tx["transaction_date"].min().date()
max_date = tx["transaction_date"].max().date()
date_range = st.sidebar.date_input("Transaction Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

f_customers = customers.copy()
if selected_card != "All":
    f_customers = f_customers[f_customers["card_type"] == selected_card]
if selected_gender != "All":
    f_customers = f_customers[f_customers["gender"] == selected_gender]
if selected_risk != "All":
    f_customers = f_customers[f_customers["churn_risk_segment"] == selected_risk]

valid_customer_ids = set(f_customers["customer_id"])
f_tx = tx[tx["customer_id"].isin(valid_customer_ids)].copy()

if len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    f_tx = f_tx[(f_tx["transaction_date"] >= start_date) & (f_tx["transaction_date"] <= end_date)]

total_customers = f_customers["customer_id"].nunique()
total_spend = f_tx["transaction_amount"].sum()
total_txns = len(f_tx)
avg_txn = f_tx["transaction_amount"].mean() if total_txns else 0
avg_limit = f_customers["credit_limit"].mean() if len(f_customers) else 0
avg_util = f_customers["utilization_ratio"].mean() if len(f_customers) else 0

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Customers", f"{total_customers:,}")
c2.metric("Total Spend", f"${total_spend:,.0f}")
c3.metric("Transactions", f"{total_txns:,}")
c4.metric("Avg Txn Value", f"${avg_txn:,.2f}")
c5.metric("Avg Credit Limit", f"${avg_limit:,.0f}")
c6.metric("Avg Utilization", f"{avg_util*100:.1f}%")

st.divider()

monthly = f_tx.assign(month=f_tx["transaction_date"].dt.to_period("M").astype(str)).groupby("month", as_index=False)["transaction_amount"].sum()
fig_monthly = px.line(monthly, x="month", y="transaction_amount", markers=True, title="Monthly Transaction Spend")
fig_monthly.update_layout(xaxis_title="", yaxis_title="Spend ($)")
st.plotly_chart(fig_monthly, use_container_width=True)

left, right = st.columns(2)
with left:
    by_card = f_customers.groupby("card_type", as_index=False)["customer_id"].nunique().rename(columns={"customer_id": "customers"})
    st.plotly_chart(px.bar(by_card, x="card_type", y="customers", title="Customers by Card Type"), use_container_width=True)

with right:
    by_category = f_tx.groupby("transaction_category", as_index=False)["transaction_amount"].sum().sort_values("transaction_amount", ascending=False)
    fig_cat = px.bar(by_category, x="transaction_category", y="transaction_amount", title="Spend by Transaction Category")
    fig_cat.update_layout(xaxis_title="", yaxis_title="Spend ($)")
    st.plotly_chart(fig_cat, use_container_width=True)

left, right = st.columns(2)
with left:
    risk_df = f_customers.groupby("churn_risk_segment", as_index=False)["customer_id"].nunique().rename(columns={"customer_id": "customers"})
    st.plotly_chart(px.pie(risk_df, names="churn_risk_segment", values="customers", title="Customer Churn-Risk Segmentation", hole=0.45), use_container_width=True)

with right:
    channel_df = f_tx.groupby("channel", as_index=False)["transaction_amount"].sum().sort_values("transaction_amount", ascending=False)
    fig_channel = px.bar(channel_df, x="channel", y="transaction_amount", title="Spend by Transaction Channel")
    fig_channel.update_layout(xaxis_title="", yaxis_title="Spend ($)")
    st.plotly_chart(fig_channel, use_container_width=True)

st.subheader("Top 10 Customers by Spend")
top_customers = (
    f_tx.groupby("customer_id", as_index=False)["transaction_amount"].sum()
    .sort_values("transaction_amount", ascending=False).head(10)
    .merge(f_customers[["customer_id", "card_type", "annual_income", "credit_limit", "churn_risk_segment"]], on="customer_id", how="left")
    .rename(columns={"transaction_amount": "total_spend"})
)
st.dataframe(top_customers, use_container_width=True, hide_index=True)

st.subheader("Key Business Insights")
if len(f_tx):
    top_cat = by_category.iloc[0]
    top_channel = channel_df.iloc[0]
    high_risk_count = (f_customers["churn_risk_segment"] == "High").sum()
    high_risk_pct = (high_risk_count / len(f_customers) * 100) if len(f_customers) else 0
    premium_spend = (
        f_tx.merge(f_customers[["customer_id", "card_type"]], on="customer_id", how="left")
        .groupby("card_type")["transaction_amount"].sum().sort_values(ascending=False)
    )
    st.markdown(f"""
- **{top_cat['transaction_category']}** is the highest-spend category in the current filter.
- **{top_channel['channel']}** is the leading transaction channel by spend.
- **{high_risk_count:,} customers ({high_risk_pct:.1f}%)** fall into the high churn-risk segment.
- **Average credit utilization is {avg_util*100:.1f}%**.
- Highest-spend card segment in the current filter: **{premium_spend.index[0] if len(premium_spend) else 'N/A'}**.
""")
else:
    st.info("No transactions match the selected filters.")
