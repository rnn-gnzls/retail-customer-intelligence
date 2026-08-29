import pandas as pd
from pathlib import Path

# CONFIGURATION
BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data" / "raw" / "online-retail.csv"
OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "retail-clean.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# LOAD DATA
print("=" * 70)
print("LOADING RAW DATA")
print("=" * 70)

df = pd.read_csv(
    RAW_FILE,
    encoding="ISO-8859-1"
)

print(f"Rows loaded: {len(df):,}")

# STANDARDIZE COLUMN NAMES
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print("\nColumns:")
print(list(df.columns))

# DATA TYPE CONVERSION
df["invoicedate"] = pd.to_datetime(
    df["invoicedate"],
    errors="coerce"
)

df["customerid"] = pd.to_numeric(
    df["customerid"],
    errors="coerce"
)

df["quantity"] = pd.to_numeric(
    df["quantity"],
    errors="coerce"
)

df["unitprice"] = pd.to_numeric(
    df["unitprice"],
    errors="coerce"
)

# DATA QUALITY CHECK
print("\n" + "=" * 70)
print("INITIAL DATA QUALITY")
print("=" * 70)

print(f"Missing Customer IDs: {df['customerid'].isna().sum():,}")
print(f"Missing Descriptions: {df['description'].isna().sum():,}")
print(f"Invalid Dates: {df['invoicedate'].isna().sum():,}")
print(f"Duplicate Rows: {df.duplicated().sum():,}")

# IDENTIFY TRANSACTION TYPES
df["invoice_str"] = df["invoiceno"].astype(str).str.strip()

df["is_cancellation"] = (
    df["invoice_str"].str.upper().str.startswith("C")
)

df["is_negative_quantity"] = df["quantity"] < 0

# REMOVE INVALID TRANSACTIONS
# Remove rows without essential analytical information
df = df[
    df["invoicedate"].notna()
    & df["stockcode"].notna()
    & df["quantity"].notna()
    & df["unitprice"].notna()
]

# Remove non-positive prices
df = df[df["unitprice"] > 0]

# Remove cancellation/negative sales transactions
sales_df = df[
    (~df["is_cancellation"])
    & (df["quantity"] > 0)
].copy()

print("\n" + "=" * 70)
print("SALES TRANSACTION FILTER")
print("=" * 70)

print(f"Rows after filtering: {len(sales_df):,}")

# CUSTOMER FILTER
# Customer analytics requires a valid Customer ID
sales_df = sales_df[
    sales_df["customerid"].notna()
].copy()

# Convert Customer ID to integer
sales_df["customerid"] = sales_df["customerid"].astype(int)

print(f"Rows with valid Customer ID: {len(sales_df):,}")

# REMOVE DUPLICATES
before_duplicates = len(sales_df)

sales_df = sales_df.drop_duplicates()

duplicates_removed = before_duplicates - len(sales_df)

print(f"Duplicate rows removed: {duplicates_removed:,}")

# FEATURE ENGINEERING
sales_df["revenue"] = (
    sales_df["quantity"] *
    sales_df["unitprice"]
)

sales_df["order_date"] = (
    sales_df["invoicedate"].dt.date
)

sales_df["order_month"] = (
    sales_df["invoicedate"]
    .dt.to_period("M")
    .astype(str)
)

sales_df["order_year"] = (
    sales_df["invoicedate"].dt.year
)

sales_df["order_month_number"] = (
    sales_df["invoicedate"].dt.month
)

sales_df["day_of_week"] = (
    sales_df["invoicedate"]
    .dt.day_name()
)

sales_df["hour"] = (
    sales_df["invoicedate"].dt.hour
)

# CUSTOMER FIRST / LAST PURCHASE
customer_first_purchase = (
    sales_df
    .groupby("customerid")["invoicedate"]
    .transform("min")
)

customer_last_purchase = (
    sales_df
    .groupby("customerid")["invoicedate"]
    .transform("max")
)

sales_df["first_purchase_date"] = (
    customer_first_purchase.dt.date
)

sales_df["last_purchase_date"] = (
    customer_last_purchase.dt.date
)

sales_df["first_purchase_month"] = (
    customer_first_purchase
    .dt.to_period("M")
    .astype(str)
)

sales_df["customer_order_count"] = (
    sales_df
    .groupby("customerid")["invoiceno"]
    .transform("nunique")
)

# CUSTOMER TYPE
sales_df["customer_type"] = sales_df[
    "customer_order_count"
].apply(
    lambda x: "Repeat Customer"
    if x > 1
    else "One-Time Customer"
)

# VALIDATION
print("\n" + "=" * 70)
print("FINAL DATA VALIDATION")
print("=" * 70)

print(f"Rows: {len(sales_df):,}")
print(f"Columns: {len(sales_df.columns):,}")
print(f"Missing values: {sales_df.isna().sum().sum():,}")
print(f"Duplicate rows: {sales_df.duplicated().sum():,}")

print("\nDate range:")
print(f"Start: {sales_df['invoicedate'].min()}")
print(f"End:   {sales_df['invoicedate'].max()}")

print("\nBusiness metrics:")

print(
    f"Revenue: £{sales_df['revenue'].sum():,.2f}"
)

print(
    f"Customers: "
    f"{sales_df['customerid'].nunique():,}"
)

print(
    f"Orders: "
    f"{sales_df['invoiceno'].nunique():,}"
)

print(
    f"Products: "
    f"{sales_df['stockcode'].nunique():,}"
)

print(
    f"Countries: "
    f"{sales_df['country'].nunique():,}"
)

print("\nCustomer types:")

print(
    sales_df["customer_type"]
    .value_counts()
    .to_string()
)

# SAVE CLEAN DATA
sales_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 70)
print("CLEANING COMPLETE")
print("=" * 70)

print(f"Saved to:")
print(OUTPUT_FILE)