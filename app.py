import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from data_generator import ensure_csvs

st.set_page_config(
    page_title="Credit Card Customer Analytics",
    page_icon="💳",
    layout="wide",
)

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

value_segments = ["All", "High Value", "Growth", "Core", "Low Engagement"]
selected_value = st.sidebar.selectbox("Customer Value Segment", value_segments)

min_date = tx["transaction_date"].min().date()
max_date = tx["transaction_date"].max().date()
date_range = st.sidebar.date_input(
    "Transaction Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

f_customers = customers.copy()
if selected_card != "All":
    f_customers = f_customers[f_customers["card_type"] == selected_card]
if selected_gender != "All":
    f_customers = f_customers[f_customers["gender"] == selected_gender]
if selected_risk != "All":
    f_customers = f_customers[f_customers["churn_risk_segment"] == selected_risk]
if selected_value != "All":
    f_customers = f_customers[f_customers["customer_value_segment"] == selected_value]

valid_customer_ids = set(f_customers["customer_id"])
f_tx = tx[tx["customer_id"].isin(valid_customer_ids)].copy()

if len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    f_tx = f_tx[
        (f_tx["transaction_date"] >= start_date)
        & (f_tx["transaction_date"] <= end_date)
    ]

total_customers = f_customers["customer_id"].nunique()
total_spend = f_tx["transaction_amount"].sum()
total_txns = len(f_tx)
avg_txn = f_tx["transaction_amount"].mean() if total_txns else 0
avg_limit = f_customers["credit_limit"].mean() if len(f_customers) else 0
avg_util = f_customers["utilization_ratio"].mean() if len(f_customers) else 0

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Customers", f"{total_customers:,}")
c2.metric("Total Spend", f"USD {total_spend:,.0f}")
c3.metric("Transactions", f"{total_txns:,}")
c4.metric("Avg Txn Value", f"USD {avg_txn:,.2f}")
c5.metric("Avg Credit Limit", f"USD {avg_limit:,.0f}")
c6.metric("Avg Utilization", f"{avg_util*100:.1f}%")

st.divider()

overview_tab, segment_tab, risk_tab = st.tabs(
    ["Executive Overview", "Customer Segmentation", "Risk & Engagement"]
)

with overview_tab:
    monthly = (
        f_tx.assign(month=f_tx["transaction_date"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)["transaction_amount"]
        .sum()
    )
    fig_monthly = px.line(
        monthly,
        x="month",
        y="transaction_amount",
        markers=True,
        title="Monthly Transaction Spend",
    )
    fig_monthly.update_layout(xaxis_title="", yaxis_title="Spend (USD)")
    st.plotly_chart(fig_monthly, use_container_width=True)

    left, right = st.columns(2)

    with left:
        by_card = (
            f_customers.groupby("card_type", as_index=False)["customer_id"]
            .nunique()
            .rename(columns={"customer_id": "customers"})
        )
        st.plotly_chart(
            px.bar(
                by_card,
                x="card_type",
                y="customers",
                title="Customers by Card Type",
            ),
            use_container_width=True,
        )

    with right:
        by_category = (
            f_tx.groupby("transaction_category", as_index=False)["transaction_amount"]
            .sum()
            .sort_values("transaction_amount", ascending=False)
        )
        fig_cat = px.bar(
            by_category,
            x="transaction_category",
            y="transaction_amount",
            title="Spend by Transaction Category",
        )
        fig_cat.update_layout(xaxis_title="", yaxis_title="Spend (USD)")
        st.plotly_chart(fig_cat, use_container_width=True)

    channel_df = (
        f_tx.groupby("channel", as_index=False)["transaction_amount"]
        .sum()
        .sort_values("transaction_amount", ascending=False)
    )
    fig_channel = px.bar(
        channel_df,
        x="channel",
        y="transaction_amount",
        title="Spend by Transaction Channel",
    )
    fig_channel.update_layout(xaxis_title="", yaxis_title="Spend (USD)")
    st.plotly_chart(fig_channel, use_container_width=True)

with segment_tab:
    left, right = st.columns(2)

    with left:
        value_df = (
            f_customers.groupby("customer_value_segment", as_index=False)["customer_id"]
            .nunique()
            .rename(columns={"customer_id": "customers"})
        )
        st.plotly_chart(
            px.bar(
                value_df,
                x="customer_value_segment",
                y="customers",
                title="Customer Value Segments",
            ),
            use_container_width=True,
        )

    with right:
        segment_spend = (
            f_tx.merge(
                f_customers[["customer_id", "customer_value_segment"]],
                on="customer_id",
                how="left",
            )
            .groupby("customer_value_segment", as_index=False)["transaction_amount"]
            .sum()
            .sort_values("transaction_amount", ascending=False)
        )
        fig_segment_spend = px.bar(
            segment_spend,
            x="customer_value_segment",
            y="transaction_amount",
            title="Spend by Customer Value Segment",
        )
        fig_segment_spend.update_layout(xaxis_title="", yaxis_title="Spend (USD)")
        st.plotly_chart(fig_segment_spend, use_container_width=True)

    st.subheader("Top 10 Customers by Spend")
    top_customers = (
        f_tx.groupby("customer_id", as_index=False)["transaction_amount"]
        .sum()
        .sort_values("transaction_amount", ascending=False)
        .head(10)
        .merge(
            f_customers[
                [
                    "customer_id",
                    "card_type",
                    "annual_income",
                    "credit_limit",
                    "customer_value_segment",
                    "churn_risk_segment",
                ]
            ],
            on="customer_id",
            how="left",
        )
        .rename(columns={"transaction_amount": "total_spend"})
    )
    st.dataframe(top_customers, use_container_width=True, hide_index=True)

with risk_tab:
    left, right = st.columns(2)

    with left:
        risk_df = (
            f_customers.groupby("churn_risk_segment", as_index=False)["customer_id"]
            .nunique()
            .rename(columns={"customer_id": "customers"})
        )
        st.plotly_chart(
            px.pie(
                risk_df,
                names="churn_risk_segment",
                values="customers",
                title="Customer Churn-Risk Segmentation",
                hole=0.45,
            ),
            use_container_width=True,
        )

    with right:
        status_df = (
            f_customers.groupby("customer_status", as_index=False)["customer_id"]
            .nunique()
            .rename(columns={"customer_id": "customers"})
        )
        st.plotly_chart(
            px.pie(
                status_df,
                names="customer_status",
                values="customers",
                title="Active vs Inactive Customers",
                hole=0.45,
            ),
            use_container_width=True,
        )

    high_util = (
        f_customers.loc[
            f_customers["utilization_ratio"] >= 0.70,
            [
                "customer_id",
                "card_type",
                "credit_limit",
                "outstanding_balance",
                "utilization_ratio",
                "customer_value_segment",
                "churn_risk_segment",
            ],
        ]
        .sort_values("utilization_ratio", ascending=False)
        .head(20)
    )
    st.subheader("High Utilization Customers")
    st.dataframe(high_util, use_container_width=True, hide_index=True)

st.subheader("Key Business Insights")

if len(f_tx):
    by_category = (
        f_tx.groupby("transaction_category", as_index=False)["transaction_amount"]
        .sum()
        .sort_values("transaction_amount", ascending=False)
    )
    channel_df = (
        f_tx.groupby("channel", as_index=False)["transaction_amount"]
        .sum()
        .sort_values("transaction_amount", ascending=False)
    )

    top_cat = by_category.iloc[0]
    top_channel = channel_df.iloc[0]
    high_risk_count = (f_customers["churn_risk_segment"] == "High").sum()
    high_risk_pct = (
        high_risk_count / len(f_customers) * 100 if len(f_customers) else 0
    )
    high_value_count = (f_customers["customer_value_segment"] == "High Value").sum()
    high_value_pct = (
        high_value_count / len(f_customers) * 100 if len(f_customers) else 0
    )

    st.markdown(
        f"""
- **{top_cat['transaction_category']}** is the highest-spend category in the current filter.
- **{top_channel['channel']}** is the leading transaction channel by spend.
- **{high_risk_count:,} customers ({high_risk_pct:.1f}%)** fall into the high churn-risk segment.
- **{high_value_count:,} customers ({high_value_pct:.1f}%)** are classified as High Value.
- **Average credit utilization is {avg_util*100:.1f}%**.
"""
    )
else:
    st.info("No transactions match the selected filters.")

st.caption(
    "Portfolio note: churn-risk and customer-value segments are analytical rules "
    "for demonstration, not production credit-risk or lending models."
)
