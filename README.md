# Customer Churn Analysis

An end-to-end data analytics project focused on understanding customer churn, identifying retention risks, and uncovering actionable business insights using Python, PostgreSQL, Tableau, and Streamlit.

## 🔗 Project Links

- **Live Interactive Dashboard:** [View Streamlit Dashboard](https://customer-churn-analysis-fypxmfgc33shmtfsgsvfm2.streamlit.app/)
- **GitHub Repository:** [Customer Churn Analysis](https://github.com/ashish28-art/customer-churn-analysis)
- **Tableau Dashboard:** Add your published Tableau dashboard link here.

## 📌 Business Problem

Customer churn occurs when customers stop using a company's services. High churn can affect revenue, customer lifetime value, and long-term business growth.

The objective of this project is to analyze customer data, identify customer segments associated with higher churn, and communicate findings through interactive dashboards.

## 🎯 Project Objectives

- Measure overall customer churn and retention.
- Analyze churn across contract types and payment methods.
- Investigate the relationship between customer tenure and churn.
- Explore customer behavior using Python and SQL.
- Build interactive dashboards for communicating business insights.
- Develop data-driven recommendations to support customer retention.

## 🛠️ Tools & Technologies

- **Python:** Data cleaning and exploratory data analysis
- **Pandas:** Data manipulation and analysis
- **PostgreSQL:** Data storage and SQL-based business analysis
- **Tableau:** Interactive business intelligence dashboard
- **Streamlit:** Interactive web dashboard
- **Plotly:** Interactive charts and visualizations
- **SQLAlchemy:** Database connectivity
- **Git & GitHub:** Version control and project management
- **Supabase:** Hosted PostgreSQL database

## 📊 Dataset

The project uses the Telco Customer Churn dataset containing 7,043 customer records and 21 columns.

The dataset includes information about:

- Customer demographics
- Tenure and services subscribed
- Contract type
- Payment method
- Monthly and total charges
- Churn status

## 🔍 Key Findings

### Overall Churn

- Total customers: **7,043**
- Churned customers: **1,869**
- Retained customers: **5,174**
- Overall churn rate: **26.54%**

### Churn by Contract Type

| Contract Type | Customers Churned | Churn Rate |
|---|---:|---:|
| Month-to-month | 1,655 | 42.71% |
| One year | 166 | 11.27% |
| Two year | 48 | 2.83% |

Month-to-month customers have a substantially higher observed churn rate than customers on longer-term contracts.

### Churn by Payment Method

| Payment Method | Customers Churned | Churn Rate |
|---|---:|---:|
| Electronic check | 1,071 | 45.29% |
| Mailed check | 308 | 19.11% |
| Bank transfer (automatic) | 258 | 16.71% |
| Credit card (automatic) | 232 | 15.24% |

Customers using electronic checks have the highest observed churn rate among the payment-method groups.

### Churn by Tenure

| Tenure Group | Customers | Churned | Churn Rate |
|---|---:|---:|---:|
| New (0–12 months) | 2,186 | 1,037 | 47.44% |
| Medium (13–48 months) | 2,618 | 619 | 23.64% |
| Long (49–72 months) | 2,239 | 213 | 9.51% |

Newer customers have a higher observed churn rate, highlighting the importance of early customer engagement and onboarding.

*These findings show associations in the dataset; they do not establish that contract type, payment method, or tenure independently causes churn.*

## 📈 Dashboard Features

The Streamlit dashboard includes:

- KPI cards for total customers, churned customers, churn rate, and average monthly charges
- Interactive customer churn distribution chart
- Churn rate comparison by contract type
- Churn rate comparison by payment method
- Filters for contract type and internet service
- Dynamic business insights based on selected filters

## 💡 Business Recommendations

Based on the observed patterns, businesses could consider:

1. **Improve early customer retention:** Introduce onboarding support and proactive engagement during the first year.
2. **Review month-to-month customer retention:** Test targeted retention offers and communicate the value of longer-term plans.
3. **Investigate electronic-check churn:** Explore whether payment experience, customer characteristics, or other factors help explain the higher churn rate.
4. **Use data-driven retention campaigns:** Segment customers by tenure, contract, and service characteristics to prioritize further investigation.
5. **Measure campaign effectiveness:** Track retention outcomes to evaluate whether interventions actually reduce churn.

These recommendations are hypotheses to test, not proven causal effects.

## ⚙️ Project Structure

```text
Customer-Churn/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   └── 01_data_understanding.ipynb
├── python/
│   ├── app.py
│   └── data_cleaning.py
├── sql/
│   ├── 01_schema.sql
│   └── 02_business_analysis.sql
├── requirements.txt
└── README.md
```

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/ashish28-art/customer-churn-analysis.git
cd customer-churn-analysis
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create a PostgreSQL database named `churn_db`, then execute the schema and business-analysis SQL files as needed.

Configure the database connection in `python/app.py` for your local environment. The default local connection in this project uses:

```text
postgresql+psycopg:///churn_db
```

Ensure your PostgreSQL server is running and the customer table has been populated before launching the dashboard.

### 5. Launch the dashboard

```bash
python -m streamlit run python/app.py
```

Open the local URL displayed in your terminal.

## 🔐 Security

- Never commit database passwords, connection strings, or secret configuration files.
- Use Streamlit Secrets for hosted database credentials.
- Keep virtual environments and local secrets excluded through `.gitignore`.

## 👨‍💻 About This Project

This project demonstrates an end-to-end analytics workflow, from data cleaning and SQL analysis to business intelligence visualization and deployment.

The goal was not only to build dashboards, but also to understand the data, interpret customer behavior, and communicate insights that could inform business decisions.
