import pandas as pd
from pathlib import Path

# CONFIGURATION
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_FILE = BASE_DIR / "data" / "raw" / "online-retail.csv"

# LOAD DATA
print("=" * 70)
print("LOADING DATASET")
print("=" * 70)

df = pd.read_csv(
    RAW_FILE,
    encoding="ISO-8859-1"
)

print(f"File: {RAW_FILE}")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")

# COLUMN NAMES
print("\n" + "=" * 70)
print("COLUMN NAMES")
print("=" * 70)

for i, column in enumerate(df.columns, 1):
    print(f"{i:2}. {column}")

# DATA TYPES
print("\n" + "=" * 70)
print("DATA TYPES")
print("=" * 70)

print(df.dtypes)

# MISSING VALUES
print("\n" + "=" * 70)
print("MISSING VALUES")
print("=" * 70)

missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100

missing_summary = pd.DataFrame({
    "Missing": missing,
    "Missing %": missing_pct.round(2)
})

print(missing_summary[missing_summary["Missing"] > 0])

# DUPLICATES
print("\n" + "=" * 70)
print("DUPLICATE ROWS")
print("=" * 70)

print(f"Duplicate rows: {df.duplicated().sum():,}")

# FIRST 5 ROWS
print("\n" + "=" * 70)
print("FIRST 5 ROWS")
print("=" * 70)

print(df.head().to_string())

# NUMERICAL SUMMARY
print("\n" + "=" * 70)
print("NUMERICAL SUMMARY")
print("=" * 70)

print(df.describe().to_string())

# UNIQUE VALUES
print("\n" + "=" * 70)
print("UNIQUE VALUES")
print("=" * 70)

for column in df.columns:
    print(f"{column}: {df[column].nunique(dropna=False):,} unique values")

# TRANSACTION ANALYSIS
print("\n" + "=" * 70)
print("TRANSACTION ANALYSIS")
print("=" * 70)

if "InvoiceNo" in df.columns:

    cancellations = df["InvoiceNo"].astype(str).str.startswith("C")

    print(f"Total transactions: {len(df):,}")
    print(f"Cancellation rows: {cancellations.sum():,}")
    print(
        f"Cancellation rate: "
        f"{cancellations.mean() * 100:.2f}%"
    )

if "Quantity" in df.columns:

    negative_qty = (df["Quantity"] < 0).sum()

    print(f"Negative quantity rows: {negative_qty:,}")

if "CustomerID" in df.columns:

    print(
        f"Unique customers: "
        f"{df['CustomerID'].nunique():,}"
    )

if "StockCode" in df.columns:

    print(
        f"Unique products: "
        f"{df['StockCode'].nunique():,}"
    )

if "Country" in df.columns:

    print(
        f"Unique countries: "
        f"{df['Country'].nunique():,}"
    )

# DATE ANALYSIS
print("\n" + "=" * 70)
print("DATE ANALYSIS")
print("=" * 70)

if "InvoiceDate" in df.columns:

    dates = pd.to_datetime(
        df["InvoiceDate"],
        errors="coerce"
    )

    print(f"Invalid dates: {dates.isna().sum():,}")

    if dates.notna().any():
        print(f"Start: {dates.min()}")
        print(f"End:   {dates.max()}")

# REVENUE CHECK
if "Quantity" in df.columns and "UnitPrice" in df.columns:

    revenue = df["Quantity"] * df["UnitPrice"]

    print("\n" + "=" * 70)
    print("REVENUE CHECK")
    print("=" * 70)

    print(f"Total calculated revenue: £{revenue.sum():,.2f}")
    print(f"Average transaction value: £{revenue.mean():,.2f}")

# COMPLETE
print("\n" + "=" * 70)
print("PROFILE COMPLETE")
print("=" * 70)