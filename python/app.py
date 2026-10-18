
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text

# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================
st.set_page_config(
    page_title="Customer Churn Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# 2. CUSTOM CSS
# ==================================================
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1600px;
    }

    h1 {
        font-size: 2.35rem !important;
        font-weight: 750 !important;
        letter-spacing: -1px;
    }

    h2, h3 {
        letter-spacing: -0.4px;
    }

    /* KPI cards */
    [data-testid="stMetric"] {
        background: #181B24;
        border: 1px solid #2B3040;
        padding: 20px 22px;
        border-radius: 14px;
        min-height: 115px;
    }

    [data-testid="stMetricLabel"] {
        color: #A6AEC2;
        font-size: 0.9rem;
    }

    [data-testid="stMetricValue"] {
        color: #F3F5FA;
        font-size: 1.9rem;
        font-weight: 700;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        border-right: 1px solid #2B3040;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        font-size: 1.25rem !important;
        letter-spacing: -0.3px;
        white-space: nowrap;
    }

    /* Chart containers */
    div[data-testid="stPlotlyChart"] {
        background: #12151D;
        border: 1px solid #252B38;
        border-radius: 14px;
        padding: 8px;
        overflow: hidden;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        min-height: 42px;
        font-weight: 600;
    }

    /* Insight messages */
    div[data-testid="stAlert"] {
        border-radius: 12px;
    }

    /* Dividers */
    hr {
        border-color: #2B3040;
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ==================================================
# 3. DATABASE CONNECTION AND HEADER
# ==================================================
try:
    db = st.secrets["database"]

    database_url = URL.create(
        "postgresql+psycopg",
        username=db["username"],
        password=db["password"],
        host=db["host"],
        port=int(db["port"]),
        database=db["dbname"],
    )

    engine = create_engine(database_url, pool_pre_ping=True)

except (KeyError, FileNotFoundError):
    engine = create_engine("postgresql+psycopg:///churn_db")

engine = create_engine(database_url)

engine = create_engine(database_url)

st.title("Customer Churn Analytics")
st.caption(
    "Understanding customer retention and churn behavior"
)

# ==================================================
# 4. LOAD DATA
# ==================================================
try:
    with engine.connect() as connection:
        customer_data = pd.read_sql(
            text("SELECT * FROM public.telco_customers"),
            connection
        )

    customer_data["monthly_charges"] = pd.to_numeric(
        customer_data["monthly_charges"],
        errors="coerce"
    )

    # ==================================================
    # 5. SIDEBAR FILTERS
    # ==================================================
    st.sidebar.title("Customer Filters")
    st.sidebar.caption("Explore customer segments")

    contract_options = sorted(
        customer_data["contract"].dropna().unique().tolist()
    )

    selected_contracts = st.sidebar.multiselect(
        "Contract Type",
        options=contract_options,
        default=contract_options
    )

    internet_options = sorted(
        customer_data["internet_service"].dropna().unique().tolist()
    )

    selected_internet = st.sidebar.multiselect(
        "Internet Service",
        options=internet_options,
        default=internet_options
    )

    if st.sidebar.button(
        "Reset Filters",
        use_container_width=True
    ):
        st.rerun()

    # Apply filters
    filtered_data = customer_data[
        customer_data["contract"].isin(selected_contracts)
        & customer_data["internet_service"].isin(selected_internet)
    ].copy()

    if filtered_data.empty:
        st.warning(
            "No customers match these filters. "
            "Please select at least one option in each filter."
        )
        st.stop()

    # ==================================================
    # 6. CALCULATE KPIs
    # ==================================================
    total_customers = len(filtered_data)

    churned_customers = int(
        (filtered_data["churn"] == "Yes").sum()
    )

    churn_rate = (
        churned_customers / total_customers * 100
        if total_customers else 0
    )

    avg_monthly_charges = filtered_data[
        "monthly_charges"
    ].mean()

    # ==================================================
    # 7. KPI CARDS
    # ==================================================
    st.subheader("Business Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Customers",
        f"{total_customers:,}"
    )

    col2.metric(
        "Churned Customers",
        f"{churned_customers:,}"
    )

    col3.metric(
        "Churn Rate",
        f"{churn_rate:.2f}%"
    )

    col4.metric(
        "Avg. Monthly Charges",
        (
            f"{avg_monthly_charges:.2f}"
            if pd.notna(avg_monthly_charges)
            else "N/A"
        )
    )

    st.divider()
    st.subheader("Customer Insights")

    # ==================================================
    # 8. CHURN DISTRIBUTION
    # ==================================================
    churn_data = (
        filtered_data.groupby("churn")
        .size()
        .reset_index(name="customer_count")
    )

    churn_data["status"] = churn_data["churn"].map({
        "No": "Stayed",
        "Yes": "Churned"
    })

    fig_churn = px.pie(
        churn_data,
        names="status",
        values="customer_count",
        hole=0.65,
        color="status",
        color_discrete_map={
            "Stayed": "#22C55E",
            "Churned": "#EF4444"
        },
        title="Customer Churn Distribution"
    )

    fig_churn.update_traces(
        textinfo="percent",
        hovertemplate=(
            "%{label}<br>"
            "Customers: %{value:,}<br>"
            "Share: %{percent}"
            "<extra></extra>"
        )
    )

    fig_churn.update_layout(
        template="plotly_dark",
        paper_bgcolor="#12151D",
        plot_bgcolor="#12151D",
        font=dict(
            family="Arial, sans-serif",
            color="#E5E7EB"
        ),
        height=380,
        margin=dict(t=60, b=20, l=20, r=20),
        legend_title_text="Customer Status"
    )

    # ==================================================
    # 9. CHURN RATE BY CONTRACT
    # ==================================================
    contract_data = (
        filtered_data.groupby("contract")
        .agg(
            total_customers=("customer_id", "count"),
            churned_customers=(
                "churn",
                lambda values: (values == "Yes").sum()
            )
        )
        .reset_index()
    )

    contract_data["churn_rate"] = (
        contract_data["churned_customers"]
        / contract_data["total_customers"]
        * 100
    )

    contract_data = contract_data.sort_values(
        "churn_rate",
        ascending=False
    )

    fig_contract = px.bar(
        contract_data,
        x="contract",
        y="churn_rate",
        color="contract",
        text="churn_rate",
        color_discrete_map={
            "Month-to-month": "#EF4444",
            "One year": "#3B82F6",
            "Two year": "#22C55E"
        },
        title="Churn Rate by Contract Type",
        labels={
            "contract": "Contract Type",
            "churn_rate": "Churn Rate (%)"
        },
        hover_data={
            "total_customers": True,
            "churned_customers": True,
            "churn_rate": ":.2f"
        }
    )

    fig_contract.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    contract_max = float(
        contract_data["churn_rate"].max()
    )

    fig_contract.update_layout(
        template="plotly_dark",
        paper_bgcolor="#12151D",
        plot_bgcolor="#12151D",
        font=dict(
            family="Arial, sans-serif",
            color="#E5E7EB"
        ),
        height=380,
        showlegend=False,
        yaxis_title="Churn Rate (%)",
        xaxis_title="",
        yaxis_range=[0, max(10, min(100, contract_max * 1.2))],
        margin=dict(t=60, b=30, l=20, r=20)
    )

    # ==================================================
    # 10. DISPLAY FIRST TWO CHARTS
    # ==================================================
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.plotly_chart(
            fig_churn,
            use_container_width=True
        )

    with chart_col2:
        st.plotly_chart(
            fig_contract,
            use_container_width=True
        )

    # ==================================================
    # 11. CHURN RATE BY PAYMENT METHOD
    # ==================================================
    payment_data = (
        filtered_data.groupby("payment_method")
        .agg(
            total_customers=("customer_id", "count"),
            churned_customers=(
                "churn",
                lambda values: (values == "Yes").sum()
            )
        )
        .reset_index()
    )

    payment_data["churn_rate"] = (
        payment_data["churned_customers"]
        / payment_data["total_customers"]
        * 100
    )

    payment_data = payment_data.sort_values(
        "churn_rate",
        ascending=True
    )

    fig_payment = px.bar(
        payment_data,
        x="churn_rate",
        y="payment_method",
        orientation="h",
        text="churn_rate",
        color="churn_rate",
        color_continuous_scale=[
            "#FCA5A5",
            "#EF4444",
            "#991B1B"
        ],
        title="Churn Rate by Payment Method",
        labels={
            "payment_method": "Payment Method",
            "churn_rate": "Churn Rate (%)"
        },
        hover_data={
            "total_customers": True,
            "churned_customers": True,
            "churn_rate": ":.2f"
        }
    )

    fig_payment.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
        cliponaxis=False
    )

    payment_max = float(
        payment_data["churn_rate"].max()
    )

    fig_payment.update_layout(
        template="plotly_dark",
        paper_bgcolor="#12151D",
        plot_bgcolor="#12151D",
        font=dict(
            family="Arial, sans-serif",
            color="#E5E7EB"
        ),
        height=400,
        showlegend=False,
        coloraxis_showscale=False,
        xaxis_title="Churn Rate (%)",
        yaxis_title="",
        xaxis_range=[0, max(10, min(100, payment_max * 1.2))],
        margin=dict(t=60, b=30, l=20, r=50)
    )

    st.plotly_chart(
        fig_payment,
        use_container_width=True
    )

    # ==================================================
    # 12. DYNAMIC BUSINESS INSIGHTS
    # ==================================================
    st.divider()
    st.subheader("Key Insights")

    insight_col1, insight_col2 = st.columns(2)

    if not contract_data.empty:
        highest_contract = contract_data.iloc[0]

        with insight_col1:
            st.info(
                f"**Highest-churn contract:** "
                f"{highest_contract['contract']} "
                f"({highest_contract['churn_rate']:.2f}%)."
            )

    if not payment_data.empty:
        highest_payment = payment_data.iloc[-1]

        with insight_col2:
            st.info(
                f"**Highest-churn payment method:** "
                f"{highest_payment['payment_method']} "
                f"({highest_payment['churn_rate']:.2f}%)."
            )

    st.caption(
        "These are observed associations within the selected customers. "
        "They do not establish that contract type or payment method "
        "causes customer churn."
    )

except Exception as error:
    st.error("Unable to load the dashboard.")
    st.exception(error)
