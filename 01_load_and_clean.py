import gspread
import pandas as pd
from google.oauth2.service_account import Credentials


# --------------------------------------------------
# 1. CONNECT TO GOOGLE SHEETS
# --------------------------------------------------

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES
)

gc = gspread.authorize(credentials)

print("Connected to Google Sheets!")


# --------------------------------------------------
# 2. OPEN THE SUPERSTORE GOOGLE SHEET
# --------------------------------------------------

spreadsheet = gc.open("sup")

worksheet = spreadsheet.sheet1

print(f"Loaded worksheet: {worksheet.title}")


# --------------------------------------------------
# 3. LOAD GOOGLE SHEETS DATA INTO PANDAS
# --------------------------------------------------

data = worksheet.get_all_records()

df = pd.DataFrame(data)

print(f"Rows loaded: {len(df):,}")
print(f"Columns loaded: {len(df.columns)}")


# --------------------------------------------------
# 4. CLEAN COLUMN NAMES
# --------------------------------------------------

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print("\nColumn names:")
print(df.columns.tolist())


# --------------------------------------------------
# 5. CONVERT DATE COLUMNS
# --------------------------------------------------

df["order_date"] = pd.to_datetime(
    df["order_date"],
    errors="coerce"
)

df["ship_date"] = pd.to_datetime(
    df["ship_date"],
    errors="coerce"
)


# --------------------------------------------------
# 6. CONVERT NUMERIC COLUMNS
# --------------------------------------------------

numeric_columns = [
    "sales",
    "quantity",
    "discount",
    "profit"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# --------------------------------------------------
# 7. CHECK FOR MISSING VALUES
# --------------------------------------------------

missing_values = df.isna().sum()

print("\nMissing values:")
print(missing_values[missing_values > 0])


# --------------------------------------------------
# 8. VALIDATE PROFIT MARGIN
# --------------------------------------------------

df["profit_margin"] = df["profit"] / df["sales"]

print("\nProfit margin validation:")
print(
    df[
        [
            "sales",
            "profit",
            "profit_margin"
        ]
    ].head()
)


# --------------------------------------------------
# 9. BASIC DATA VALIDATION
# --------------------------------------------------

print("\nData validation:")
print(f"Total rows: {len(df):,}")
print(f"Unique orders: {df['order_id'].nunique():,}")
print(f"Unique customers: {df['customer_id'].nunique():,}")
print(f"Total sales: ${df['sales'].sum():,.2f}")
print(f"Total profit: ${df['profit'].sum():,.2f}")


# --------------------------------------------------
# 10. FINAL DATA PREVIEW
# --------------------------------------------------

print("\nCleaned data:")
print(df.head())


# --------------------------------------------------
# 11. SAVE CLEANED DATA TO CSV
# --------------------------------------------------
df.to_csv("cleaned_superstore.csv", index=False)
print("\nCleaned data saved to 'cleaned_superstore.csv'.")