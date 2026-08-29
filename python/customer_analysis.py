import pandas as pd
from pathlib import Path

# CONFIGURATION
BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "retail-clean.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "customer-analysis.csv"
)

# LOAD DATA
print("=" * 70)
print("CUSTOMER ANALYTICS")
print("=" * 70)

df = pd.read_csv(INPUT_FILE)

df["invoicedate"] = pd.to_datetime(df["invoicedate"])

print(f"Transactions: {len(df):,}")
print(f"Customers: {df['customerid'].nunique():,}")

# ANALYSIS DATE
analysis_date = df["invoicedate"].max()

print(f"Analysis date: {analysis_date}")

# CUSTOMER-LEVEL AGGREGATION
customer = (
    df.groupby("customerid")
    .agg(
        first_purchase_date=("invoicedate", "min"),
        last_purchase_date=("invoicedate", "max"),
        total_orders=("invoiceno", "nunique"),
        total_items=("quantity", "sum"),
        total_revenue=("revenue", "sum"),
        average_order_value=("revenue", "mean"),
        unique_products=("stockcode", "nunique"),
        unique_categories=("description", "nunique"),
        unique_countries=("country", "nunique")
    )
    .reset_index()
)

# RECENCY
customer["recency_days"] = (
    analysis_date.normalize()
    - customer["last_purchase_date"].dt.normalize()
).dt.days

# FREQUENCY
customer["frequency"] = customer["total_orders"]

# MONETARY
customer["monetary"] = customer["total_revenue"]

# CUSTOMER LIFETIME
customer["customer_lifetime_days"] = (
    customer["last_purchase_date"]
    - customer["first_purchase_date"]
).dt.days

# CUSTOMER TYPE
customer["customer_type"] = customer["total_orders"].apply(
    lambda x:
        "Repeat Customer"
        if x > 1
        else "One-Time Customer"
)

# RFM SCORING
# Recency:
# Lower number of days = better customer
customer["R_score"] = pd.qcut(
    customer["recency_days"].rank(method="first"),
    5,
    labels=[5, 4, 3, 2, 1]
).astype(int)

# Frequency:
# Higher number of orders = better customer
customer["F_score"] = pd.qcut(
    customer["frequency"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

# Monetary:
# Higher revenue = better customer
customer["M_score"] = pd.qcut(
    customer["monetary"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

# RFM SCORE
customer["rfm_score"] = (
    customer["R_score"].astype(str)
    + customer["F_score"].astype(str)
    + customer["M_score"].astype(str)
)

customer["rfm_total"] = (
    customer["R_score"]
    + customer["F_score"]
    + customer["M_score"]
)

# CUSTOMER SEGMENTS
def assign_segment(row):

    r = row["R_score"]
    f = row["F_score"]
    m = row["M_score"]

    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"

    elif r >= 3 and f >= 4 and m >= 3:
        return "Loyal Customers"

    elif r >= 4 and f >= 2 and m >= 2:
        return "Potential Loyalists"

    elif r <= 2 and f >= 3 and m >= 3:
        return "At Risk"

    elif r <= 2 and f <= 2 and m >= 3:
        return "Cannot Lose Them"

    elif r <= 2 and f <= 2:
        return "Lost Customers"

    else:
        return "Needs Attention"


customer["customer_segment"] = customer.apply(
    assign_segment,
    axis=1
)

# COHORT INFORMATION
customer["cohort_month"] = (
    customer["first_purchase_date"]
    .dt.to_period("M")
    .astype(str)
)

customer["first_purchase_year"] = (
    customer["first_purchase_date"]
    .dt.year
)

# REVENUE PERCENTAGE
total_revenue = customer["total_revenue"].sum()

customer["revenue_share_pct"] = (
    customer["total_revenue"]
    / total_revenue
    * 100
)

# VALIDATION
print("\n" + "=" * 70)
print("CUSTOMER DATASET VALIDATION")
print("=" * 70)

print(f"Customers: {len(customer):,}")
print(f"Columns: {len(customer.columns):,}")
print(f"Missing values: {customer.isna().sum().sum():,}")
print(f"Duplicate customers: {customer['customerid'].duplicated().sum():,}")

# SUMMARY
print("\n" + "=" * 70)
print("CUSTOMER SUMMARY")
print("=" * 70)

print(
    f"Total Revenue: "
    f"£{customer['total_revenue'].sum():,.2f}"
)

print(
    f"Average Customer Revenue: "
    f"£{customer['total_revenue'].mean():,.2f}"
)

print(
    f"Average Orders per Customer: "
    f"{customer['total_orders'].mean():.2f}"
)

print(
    f"Repeat Customer Rate: "
    f"{(customer['total_orders'] > 1).mean() * 100:.2f}%"
)

# RFM SEGMENTS
print("\n" + "=" * 70)
print("RFM CUSTOMER SEGMENTS")
print("=" * 70)

segment_summary = (
    customer["customer_segment"]
    .value_counts()
)

print(segment_summary.to_string())

# TOP CUSTOMERS
print("\n" + "=" * 70)
print("TOP 10 CUSTOMERS BY REVENUE")
print("=" * 70)

top_customers = (
    customer[
        [
            "customerid",
            "total_orders",
            "total_revenue",
            "average_order_value",
            "customer_segment"
        ]
    ]
    .sort_values(
        "total_revenue",
        ascending=False
    )
    .head(10)
)

print(top_customers.to_string(index=False))

# SAVE
customer.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 70)
print("CUSTOMER ANALYSIS COMPLETE")
print("=" * 70)

print("Saved to:")
print(OUTPUT_FILE)