from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from data_generator import ensure_csvs


st.set_page_config(
    page_title="Credit Card Analytics",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE = Path(__file__).parent

COLORS = {
    "navy": "#0B1628",
    "panel": "#111F35",
    "panel_alt": "#162842",
    "text": "#F4F7FB",
    "muted": "#91A4BC",
    "blue": "#4EA1FF",
    "cyan": "#55D6D0",
    "green": "#54D68C",
    "amber": "#FFC55C",
    "red": "#FF7B7B",
    "grid": "#243B57",
}


@st.cache_data
def load_data():
    return ensure_csvs(BASE)


def inject_styles():
    st.markdown(
        """
        <style>
        :root {
            --dash-panel: #111F35;
            --dash-border: #243B57;
            --dash-text: #F4F7FB;
            --dash-muted: #91A4BC;
            --dash-cyan: #55D6D0;
        }
        .stApp {
            background:
                radial-gradient(circle at 18% 0%, rgba(78,161,255,.08), transparent 26rem),
                linear-gradient(180deg, #081321 0%, #0A1728 45%, #081321 100%);
        }
        .block-container {
            max-width: 1440px;
            padding-top: 1.8rem;
            padding-bottom: 3rem;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0B1728 0%, #0A1423 100%);
            border-right: 1px solid var(--dash-border);
        }
        [data-testid="stMetric"] {
            background: linear-gradient(145deg, rgba(17,31,53,.97), rgba(12,26,44,.97));
            border: 1px solid var(--dash-border);
            border-radius: 14px;
            padding: 1rem 1.05rem;
            min-height: 112px;
            box-shadow: 0 10px 28px rgba(0,0,0,.14);
        }
        [data-testid="stMetricLabel"] {
            color: var(--dash-muted);
            font-size: .78rem;
            letter-spacing: .02em;
        }
        [data-testid="stMetricValue"] {
            color: var(--dash-text);
            font-weight: 760;
            font-size: 1.55rem;
        }
        [data-baseweb="tab-list"] {
            gap: .45rem;
            background: rgba(12,26,44,.55);
            padding: .38rem;
            border: 1px solid var(--dash-border);
            border-radius: 12px;
        }
        [data-baseweb="tab"] {
            border-radius: 9px;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        [data-baseweb="tab"][aria-selected="true"] {
            background: rgba(78,161,255,.12);
        }
        [data-testid="stDataFrame"] {
            border: 1px solid var(--dash-border);
            border-radius: 12px;
            overflow: hidden;
        }
        div[data-testid="stPlotlyChart"] {
            background: linear-gradient(145deg, rgba(17,31,53,.95), rgba(12,26,44,.95));
            border: 1px solid var(--dash-border);
            border-radius: 15px;
            padding: .25rem .35rem .1rem;
        }
        .dash-header {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            align-items: flex-end;
            padding: 1.1rem 1.25rem 1.2rem;
            margin-bottom: 1.1rem;
            background: linear-gradient(135deg, rgba(18,38,64,.94), rgba(10,27,47,.94));
            border: 1px solid var(--dash-border);
            border-radius: 18px;
        }
        .dash-kicker {
            color: var(--dash-cyan);
            text-transform: uppercase;
            letter-spacing: .13em;
            font-size: .72rem;
            font-weight: 750;
            margin-bottom: .4rem;
        }
        .dash-title {
            color: var(--dash-text);
            font-size: clamp(1.7rem, 3.2vw, 2.6rem);
            font-weight: 780;
            letter-spacing: -.035em;
            line-height: 1.08;
            margin: 0;
        }
        .dash-subtitle {
            color: var(--dash-muted);
            font-size: .95rem;
            margin-top: .55rem;
            line-height: 1.5;
        }
        .dash-badges {
            display: flex;
            gap: .45rem;
            flex-wrap: wrap;
            justify-content: flex-end;
        }
        .dash-badge {
            color: #C8D6E7;
            background: rgba(255,255,255,.035);
            border: 1px solid var(--dash-border);
            border-radius: 999px;
            padding: .38rem .62rem;
            font-size: .74rem;
            white-space: nowrap;
        }
        .section-label {
            color: var(--dash-cyan);
            text-transform: uppercase;
            letter-spacing: .12em;
            font-size: .7rem;
            font-weight: 750;
            margin: 1.05rem 0 .25rem;
        }
        .section-title {
            color: var(--dash-text);
            font-size: 1.22rem;
            font-weight: 730;
            margin-bottom: .18rem;
        }
        .section-copy {
            color: var(--dash-muted);
            font-size: .87rem;
            margin-bottom: .9rem;
        }
        .insight-grid {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: .75rem;
            margin-top: .25rem;
            margin-bottom: 1rem;
        }
        .insight-card {
            background: linear-gradient(145deg, rgba(17,31,53,.96), rgba(12,26,44,.96));
            border: 1px solid var(--dash-border);
            border-radius: 13px;
            padding: .9rem;
            min-height: 112px;
        }
        .insight-card small {
            color: var(--dash-muted);
            display: block;
            font-size: .72rem;
            margin-bottom: .45rem;
        }
        .insight-card strong {
            color: var(--dash-text);
            display: block;
            font-size: 1rem;
            line-height: 1.3;
            margin-bottom: .32rem;
        }
        .insight-card span {
            color: #AFC0D3;
            font-size: .74rem;
            line-height: 1.4;
        }
        .sidebar-brand {
            border-bottom: 1px solid var(--dash-border);
            padding-bottom: .9rem;
            margin-bottom: .8rem;
        }
        .sidebar-brand strong {
            color: var(--dash-text);
            display: block;
            font-size: 1rem;
        }
        .sidebar-brand span {
            color: var(--dash-muted);
            font-size: .76rem;
        }
        .footer-note {
            color: #7F93AB;
            font-size: .72rem;
            padding-top: 1rem;
            border-top: 1px solid rgba(36,59,87,.7);
            margin-top: 1rem;
        }
        @media (max-width: 1000px) {
            .dash-header { align-items: flex-start; flex-direction: column; }
            .dash-badges { justify-content: flex-start; }
            .insight-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        }
        @media (max-width: 640px) {
            .block-container { padding-top: 1rem; }
            .insight-grid { grid-template-columns: 1fr; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def style_figure(fig, title, subtitle=None, height=360):
    title_text = title if not subtitle else f"{title}<br><sup>{subtitle}</sup>"
    fig.update_layout(
        title={
            "text": title_text,
            "x": 0.035,
            "xanchor": "left",
            "font": {"size": 17, "color": COLORS["text"]},
        },
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter, Segoe UI, sans-serif", "color": COLORS["muted"]},
        margin={"l": 28, "r": 22, "t": 74, "b": 38},
        hoverlabel={
            "bgcolor": COLORS["panel_alt"],
            "font_color": COLORS["text"],
            "bordercolor": COLORS["grid"],
        },
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1,
        },
    )
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor=COLORS["grid"],
        tickfont={"color": COLORS["muted"]},
        title_font={"color": COLORS["muted"]},
    )
    fig.update_yaxes(
        gridcolor=COLORS["grid"],
        gridwidth=1,
        zeroline=False,
        tickfont={"color": COLORS["muted"]},
        title_font={"color": COLORS["muted"]},
    )
    return fig


inject_styles()
customers, tx = load_data()

st.sidebar.markdown(
    """
    <div class="sidebar-brand">
      <strong>Portfolio Filters</strong>
      <span>Refine the customer and transaction view</span>
    </div>
    """,
    unsafe_allow_html=True,
)

card_types = ["All"] + sorted(customers["card_type"].dropna().unique().tolist())
selected_card = st.sidebar.selectbox("Card Type", card_types)

genders = ["All"] + sorted(customers["gender"].dropna().unique().tolist())
selected_gender = st.sidebar.selectbox("Gender", genders)

risk_levels = ["All", "Low", "Medium", "High"]
selected_risk = st.sidebar.selectbox("Engagement Risk", risk_levels)

value_segments = ["All", "High Value", "Growth", "Core", "Low Engagement"]
selected_value = st.sidebar.selectbox("Customer Value", value_segments)

min_date = tx["transaction_date"].min().date()
max_date = tx["transaction_date"].max().date()
date_range = st.sidebar.date_input(
    "Transaction Period",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

st.sidebar.caption("All filters update KPIs, charts, customer tables, and insights.")

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
else:
    start_date, end_date = pd.Timestamp(min_date), pd.Timestamp(max_date)

total_customers = f_customers["customer_id"].nunique()
total_spend = f_tx["transaction_amount"].sum()
total_txns = len(f_tx)
avg_txn = f_tx["transaction_amount"].mean() if total_txns else 0
avg_limit = f_customers["credit_limit"].mean() if len(f_customers) else 0
avg_util = f_customers["utilization_ratio"].mean() if len(f_customers) else 0
active_rate = (
    (f_customers["customer_status"] == "Active").mean() * 100
    if len(f_customers)
    else 0
)

period_label = f"{start_date.strftime('%b %Y')} – {end_date.strftime('%b %Y')}"

st.markdown(
    f"""
    <div class="dash-header">
      <div>
        <div class="dash-kicker">Banking analytics dashboard</div>
        <h1 class="dash-title">Credit Card Customer & Transaction Analytics</h1>
        <div class="dash-subtitle">
          Executive view of customer value, transaction behavior, portfolio utilization,
          and engagement risk.
        </div>
      </div>
      <div class="dash-badges">
        <span class="dash-badge">{period_label}</span>
        <span class="dash-badge">{total_customers:,} customers</span>
        <span class="dash-badge">{total_txns:,} transactions</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-label">Portfolio snapshot</div>
    <div class="section-title">Executive KPIs</div>
    <div class="section-copy">Key metrics update instantly with the selected portfolio filters.</div>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Customers", f"{total_customers:,}")
c2.metric("Transaction Value", f"USD {total_spend:,.0f}")
c3.metric("Transactions", f"{total_txns:,}")
c4.metric("Avg. Transaction", f"USD {avg_txn:,.2f}")
c5.metric("Avg. Credit Limit", f"USD {avg_limit:,.0f}")
c6.metric("Avg. Utilization", f"{avg_util*100:.1f}%")

overview_tab, segment_tab, risk_tab = st.tabs(
    ["Executive Overview", "Customer Segmentation", "Risk & Engagement"]
)

with overview_tab:
    st.markdown(
        """
        <div class="section-label">Performance</div>
        <div class="section-title">Transaction & portfolio trends</div>
        <div class="section-copy">Track transaction momentum and identify the categories, card products, and channels driving portfolio activity.</div>
        """,
        unsafe_allow_html=True,
    )

    monthly = (
        f_tx.assign(month=f_tx["transaction_date"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)["transaction_amount"]
        .sum()
    )
    fig_monthly = px.line(monthly, x="month", y="transaction_amount", markers=True)
    fig_monthly.update_traces(
        line={"color": COLORS["blue"], "width": 3},
        marker={"color": COLORS["cyan"], "size": 7},
        hovertemplate="<b>%{x}</b><br>Transaction value: USD %{y:,.0f}<extra></extra>",
    )
    fig_monthly.update_yaxes(tickprefix="$", tickformat="~s")
    style_figure(
        fig_monthly,
        "Monthly Transaction Value",
        "Monthly portfolio activity across the selected period",
        height=380,
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

    left, right = st.columns(2)

    with left:
        by_card = (
            f_customers.groupby("card_type", as_index=False)["customer_id"]
            .nunique()
            .rename(columns={"customer_id": "customers"})
            .sort_values("customers", ascending=False)
        )
        fig_card = px.bar(
            by_card,
            x="card_type",
            y="customers",
            color="card_type",
            color_discrete_sequence=[
                COLORS["cyan"],
                COLORS["blue"],
                COLORS["amber"],
                "#A58BFA",
            ],
        )
        fig_card.update_traces(
            hovertemplate="<b>%{x}</b><br>Customers: %{y:,}<extra></extra>"
        )
        fig_card.update_layout(showlegend=False)
        style_figure(
            fig_card,
            "Customer Mix by Card Type",
            "Distribution of customers across card products",
        )
        st.plotly_chart(fig_card, use_container_width=True)

    with right:
        by_category = (
            f_tx.groupby("transaction_category", as_index=False)["transaction_amount"]
            .sum()
            .sort_values("transaction_amount", ascending=True)
        )
        fig_cat = px.bar(
            by_category,
            x="transaction_amount",
            y="transaction_category",
            orientation="h",
        )
        fig_cat.update_traces(
            marker_color=COLORS["blue"],
            hovertemplate="<b>%{y}</b><br>Transaction value: USD %{x:,.0f}<extra></extra>",
        )
        fig_cat.update_xaxes(tickprefix="$", tickformat="~s")
        style_figure(
            fig_cat,
            "Transaction Value by Category",
            "Where customers are spending across the portfolio",
        )
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
        color="channel",
        color_discrete_sequence=[COLORS["cyan"], COLORS["blue"], COLORS["amber"]],
    )
    fig_channel.update_traces(
        hovertemplate="<b>%{x}</b><br>Transaction value: USD %{y:,.0f}<extra></extra>"
    )
    fig_channel.update_layout(showlegend=False)
    fig_channel.update_yaxes(tickprefix="$", tickformat="~s")
    style_figure(
        fig_channel,
        "Transaction Value by Channel",
        "Digital and physical channel contribution",
        height=350,
    )
    st.plotly_chart(fig_channel, use_container_width=True)

with segment_tab:
    st.markdown(
        """
        <div class="section-label">Customer intelligence</div>
        <div class="section-title">Value segmentation</div>
        <div class="section-copy">Compare portfolio concentration and transaction contribution across customer value groups.</div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns(2)

    with left:
        value_df = (
            f_customers.groupby("customer_value_segment", as_index=False)["customer_id"]
            .nunique()
            .rename(columns={"customer_id": "customers"})
        )
        segment_order = ["High Value", "Growth", "Core", "Low Engagement"]
        value_df["customer_value_segment"] = pd.Categorical(
            value_df["customer_value_segment"],
            categories=segment_order,
            ordered=True,
        )
        value_df = value_df.sort_values("customer_value_segment")
        fig_value = px.bar(
            value_df,
            x="customer_value_segment",
            y="customers",
            color="customer_value_segment",
            color_discrete_sequence=[
                COLORS["cyan"],
                COLORS["blue"],
                COLORS["green"],
                COLORS["amber"],
            ],
        )
        fig_value.update_layout(showlegend=False)
        fig_value.update_traces(
            hovertemplate="<b>%{x}</b><br>Customers: %{y:,}<extra></extra>"
        )
        style_figure(
            fig_value,
            "Customers by Value Segment",
            "Spend-distribution based customer grouping",
        )
        st.plotly_chart(fig_value, use_container_width=True)

    with right:
        segment_spend = (
            f_tx.merge(
                f_customers[["customer_id", "customer_value_segment"]],
                on="customer_id",
                how="left",
            )
            .groupby("customer_value_segment", as_index=False)["transaction_amount"]
            .sum()
        )
        segment_spend["customer_value_segment"] = pd.Categorical(
            segment_spend["customer_value_segment"],
            categories=segment_order,
            ordered=True,
        )
        segment_spend = segment_spend.sort_values("customer_value_segment")
        fig_segment_spend = px.bar(
            segment_spend,
            x="customer_value_segment",
            y="transaction_amount",
            color="customer_value_segment",
            color_discrete_sequence=[
                COLORS["cyan"],
                COLORS["blue"],
                COLORS["green"],
                COLORS["amber"],
            ],
        )
        fig_segment_spend.update_layout(showlegend=False)
        fig_segment_spend.update_traces(
            hovertemplate="<b>%{x}</b><br>Transaction value: USD %{y:,.0f}<extra></extra>"
        )
        fig_segment_spend.update_yaxes(tickprefix="$", tickformat="~s")
        style_figure(
            fig_segment_spend,
            "Transaction Value by Segment",
            "Contribution of each customer value group",
        )
        st.plotly_chart(fig_segment_spend, use_container_width=True)

    st.markdown(
        """
        <div class="section-label">Customer detail</div>
        <div class="section-title">Top customers by transaction value</div>
        """,
        unsafe_allow_html=True,
    )

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
        .rename(
            columns={
                "customer_id": "Customer",
                "transaction_amount": "Transaction Value",
                "card_type": "Card Type",
                "annual_income": "Annual Income",
                "credit_limit": "Credit Limit",
                "customer_value_segment": "Value Segment",
                "churn_risk_segment": "Engagement Risk",
            }
        )
    )

    st.dataframe(
        top_customers.style.format(
            {
                "Transaction Value": "USD {:,.0f}",
                "Annual Income": "USD {:,.0f}",
                "Credit Limit": "USD {:,.0f}",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

with risk_tab:
    st.markdown(
        """
        <div class="section-label">Portfolio monitoring</div>
        <div class="section-title">Engagement & utilization view</div>
        <div class="section-copy">Identify customers requiring closer engagement or utilization review. These are analytical segments, not credit decisions.</div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns(2)

    with left:
        risk_df = (
            f_customers.groupby("churn_risk_segment", as_index=False)["customer_id"]
            .nunique()
            .rename(columns={"customer_id": "customers"})
        )
        fig_risk = px.pie(
            risk_df,
            names="churn_risk_segment",
            values="customers",
            hole=0.58,
            color="churn_risk_segment",
            color_discrete_map={
                "Low": COLORS["green"],
                "Medium": COLORS["amber"],
                "High": COLORS["red"],
            },
        )
        fig_risk.update_traces(
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>Customers: %{value:,}<br>Share: %{percent}<extra></extra>",
            marker={"line": {"color": COLORS["panel"], "width": 2}},
        )
        style_figure(
            fig_risk,
            "Engagement Risk Mix",
            "Rule-based portfolio segmentation",
        )
        st.plotly_chart(fig_risk, use_container_width=True)

    with right:
        status_df = (
            f_customers.groupby("customer_status", as_index=False)["customer_id"]
            .nunique()
            .rename(columns={"customer_id": "customers"})
        )
        fig_status = px.pie(
            status_df,
            names="customer_status",
            values="customers",
            hole=0.58,
            color="customer_status",
            color_discrete_map={
                "Active": COLORS["cyan"],
                "Inactive": COLORS["amber"],
            },
        )
        fig_status.update_traces(
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>Customers: %{value:,}<br>Share: %{percent}<extra></extra>",
            marker={"line": {"color": COLORS["panel"], "width": 2}},
        )
        style_figure(
            fig_status,
            "Customer Activity Status",
            f"Active customer rate: {active_rate:.1f}%",
        )
        st.plotly_chart(fig_status, use_container_width=True)

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
        .rename(
            columns={
                "customer_id": "Customer",
                "card_type": "Card Type",
                "credit_limit": "Credit Limit",
                "outstanding_balance": "Outstanding Balance",
                "utilization_ratio": "Utilization",
                "customer_value_segment": "Value Segment",
                "churn_risk_segment": "Engagement Risk",
            }
        )
    )

    st.markdown(
        """
        <div class="section-label">Attention list</div>
        <div class="section-title">High-utilization customers</div>
        """,
        unsafe_allow_html=True,
    )
    st.dataframe(
        high_util.style.format(
            {
                "Credit Limit": "USD {:,.0f}",
                "Outstanding Balance": "USD {:,.0f}",
                "Utilization": "{:.1%}",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

st.markdown(
    """
    <div class="section-label">Management summary</div>
    <div class="section-title">Key business insights</div>
    <div class="section-copy">Dynamic observations calculated from the current filter context.</div>
    """,
    unsafe_allow_html=True,
)

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
        <div class="insight-grid">
          <div class="insight-card">
            <small>Leading category</small>
            <strong>{top_cat['transaction_category']}</strong>
            <span>USD {top_cat['transaction_amount']:,.0f} transaction value in the current view.</span>
          </div>
          <div class="insight-card">
            <small>Leading channel</small>
            <strong>{top_channel['channel']}</strong>
            <span>USD {top_channel['transaction_amount']:,.0f} transaction value in the current view.</span>
          </div>
          <div class="insight-card">
            <small>High engagement risk</small>
            <strong>{high_risk_count:,} customers</strong>
            <span>{high_risk_pct:.1f}% of filtered customers.</span>
          </div>
          <div class="insight-card">
            <small>High-value segment</small>
            <strong>{high_value_count:,} customers</strong>
            <span>{high_value_pct:.1f}% of filtered customers.</span>
          </div>
          <div class="insight-card">
            <small>Average utilization</small>
            <strong>{avg_util*100:.1f}%</strong>
            <span>Portfolio-level utilization across the filtered customer set.</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.info("No transactions match the selected filters.")

st.markdown(
    """
    <div class="footer-note">
      Synthetic-data analytics demonstration. Customer value and engagement-risk segments
      are analytical rules for portfolio exploration and are not intended for lending,
      underwriting, or creditworthiness decisions.
    </div>
    """,
    unsafe_allow_html=True,
)
