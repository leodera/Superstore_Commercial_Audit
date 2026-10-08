# ============================================================
# SUPERSTORE COMMERCIAL AUDIT
# 02 - EXECUTIVE ANALYSIS
# ============================================================

import pandas as pd
from pathlib import Path


# ============================================================
# 1. LOAD CLEANED DATA
# ============================================================

df = pd.read_csv("cleaned_superstore.csv")

print("Cleaned data loaded successfully.")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")


# ============================================================
# 2. CREATE OUTPUT FOLDER
# ============================================================

output_folder = Path("analysis_outputs")
output_folder.mkdir(exist_ok=True)

print("Output folder ready.")


# ============================================================
# 3. EXECUTIVE KPIs
# ============================================================

total_sales = df["sales"].sum()

net_profit = df["profit"].sum()

total_orders = df["order_id"].nunique()

total_quantity = df["quantity"].sum()

total_customers = df["customer_id"].nunique()

profit_margin = net_profit / total_sales

average_order_value = total_sales / total_orders


# ============================================================
# 4. CREATE KPI TABLE
# ============================================================

executive_kpis = pd.DataFrame({
    "metric": [
        "Total Sales",
        "Net Profit",
        "Total Orders",
        "Total Quantity",
        "Profit Margin",
        "Total Customers",
        "Average Order Value"
    ],
    "value": [
        total_sales,
        net_profit,
        total_orders,
        total_quantity,
        profit_margin,
        total_customers,
        average_order_value
    ]
})


# ============================================================
# 5. SALES BY CATEGORY
# ============================================================

sales_by_category = (
    df.groupby("category", as_index=False)
    .agg(sales=("sales", "sum"))
    .sort_values("sales", ascending=False)
)


# ============================================================
# 6. SALES BY REGION
# ============================================================

sales_by_region = (
    df.groupby("region", as_index=False)
    .agg(sales=("sales", "sum"))
    .sort_values("sales", ascending=False)
)


# ============================================================
# 7. SALES BY CUSTOMER SEGMENT
# ============================================================

sales_by_segment = (
    df.groupby("segment", as_index=False)
    .agg(sales=("sales", "sum"))
    .sort_values("sales", ascending=False)
)


# ============================================================
# 8. MONTHLY SALES & PROFIT
# ============================================================

df["order_date"] = pd.to_datetime(df["order_date"])

monthly_sales_profit = (
    df.assign(
        year=df["order_date"].dt.year,
        month=df["order_date"].dt.month
    )
    .groupby(["year", "month"], as_index=False)
    .agg(
        sales=("sales", "sum"),
        profit=("profit", "sum")
    )
    .sort_values(["year", "month"])
)


# Create readable period
monthly_sales_profit["period"] = (
    monthly_sales_profit["year"].astype(str)
    + "-"
    + monthly_sales_profit["month"].astype(str).str.zfill(2)
)


# ============================================================
# 9. SAVE ALL EXECUTIVE OUTPUTS
# ============================================================

executive_kpis.to_csv(
    output_folder / "executive_kpis.csv",
    index=False
)

sales_by_category.to_csv(
    output_folder / "sales_by_category.csv",
    index=False
)

sales_by_region.to_csv(
    output_folder / "sales_by_region.csv",
    index=False
)

sales_by_segment.to_csv(
    output_folder / "sales_by_segment.csv",
    index=False
)

monthly_sales_profit.to_csv(
    output_folder / "monthly_sales_profit.csv",
    index=False
)


# ============================================================
# 10. DISPLAY RESULTS
# ============================================================

print("\n" + "=" * 60)
print("EXECUTIVE OVERVIEW")
print("=" * 60)

print(f"Total Sales:         ${total_sales:,.2f}")
print(f"Net Profit:          ${net_profit:,.2f}")
print(f"Total Orders:        {total_orders:,}")
print(f"Total Quantity:      {total_quantity:,}")
print(f"Profit Margin:       {profit_margin:.2%}")
print(f"Total Customers:     {total_customers:,}")
print(f"Average Order Value: ${average_order_value:,.2f}")


print("\nExecutive analysis completed successfully.")
print("Results saved to analysis_outputs/")