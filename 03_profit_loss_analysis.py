# ============================================================
# SUPERSTORE COMMERCIAL AUDIT
# 03 - PROFIT & LOSS ANALYSIS
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


# ============================================================
# 3. PROFIT & LOSS KPIs
# ============================================================

net_profit = df["profit"].sum()

gross_profit = df.loc[
    df["profit"] > 0,
    "profit"
].sum()

total_loss = df.loc[
    df["profit"] < 0,
    "profit"
].sum()


# Calculate profitability at order level
order_profitability = (
    df.groupby("order_id", as_index=False)
    .agg(
        sales=("sales", "sum"),
        profit=("profit", "sum")
    )
)

loss_making_orders_table = (
    order_profitability[
        order_profitability["profit"] < 0
    ]
    .sort_values("profit")
)

loss_making_orders = len(loss_making_orders_table)


# ============================================================
# 4. PROFIT & LOSS KPI TABLE
# ============================================================

profit_loss_kpis = pd.DataFrame({
    "metric": [
        "Net Profit",
        "Gross Profit",
        "Total Loss",
        "Loss-Making Orders"
    ],
    "value": [
        net_profit,
        gross_profit,
        total_loss,
        loss_making_orders
    ]
})


# ============================================================
# 5. PROFIT BY CATEGORY
# ============================================================

profit_by_category = (
    df.groupby("category", as_index=False)
    .agg(
        sales=("sales", "sum"),
        profit=("profit", "sum")
    )
    .sort_values("profit", ascending=False)
)


# ============================================================
# 6. PROFIT BY SUB-CATEGORY
# ============================================================

profit_by_subcategory = (
    df.groupby("sub_category", as_index=False)
    .agg(
        sales=("sales", "sum"),
        profit=("profit", "sum")
    )
    .sort_values("profit", ascending=False)
)


# ============================================================
# 7. LOSS BY REGION
# ============================================================

loss_by_region = (
    df[df["profit"] < 0]
    .groupby("region", as_index=False)
    .agg(
        sales=("sales", "sum"),
        loss=("profit", "sum")
    )
    .sort_values("loss")
)


# ============================================================
# 8. LOSS BY CUSTOMER SEGMENT
# ============================================================

loss_by_segment = (
    df[df["profit"] < 0]
    .groupby("segment", as_index=False)
    .agg(
        sales=("sales", "sum"),
        loss=("profit", "sum")
    )
    .sort_values("loss")
)


# ============================================================
# 9. CUSTOMER PROFITABILITY
# ============================================================

customer_profitability = (
    df.groupby(
        ["customer_id", "customer_name"],
        as_index=False
    )
    .agg(
        sales=("sales", "sum"),
        profit=("profit", "sum"),
        orders=("order_id", "nunique")
    )
    .sort_values("profit")
)

top_loss_making_customers = (
    customer_profitability[
        customer_profitability["profit"] < 0
    ]
    .head(10)
)


# ============================================================
# 10. PRODUCT PROFITABILITY
# ============================================================

product_profitability = (
    df.groupby(
        ["product_id", "product_name"],
        as_index=False
    )
    .agg(
        sales=("sales", "sum"),
        profit=("profit", "sum"),
        quantity=("quantity", "sum")
    )
    .sort_values("profit")
)

top_loss_making_products = (
    product_profitability[
        product_profitability["profit"] < 0
    ]
    .head(10)
)


# ============================================================
# 11. SAVE OUTPUTS
# ============================================================

profit_loss_kpis.to_csv(
    output_folder / "profit_loss_kpis.csv",
    index=False
)

profit_by_category.to_csv(
    output_folder / "profit_by_category.csv",
    index=False
)

profit_by_subcategory.to_csv(
    output_folder / "profit_by_subcategory.csv",
    index=False
)

loss_by_region.to_csv(
    output_folder / "loss_by_region.csv",
    index=False
)

loss_by_segment.to_csv(
    output_folder / "loss_by_segment.csv",
    index=False
)

top_loss_making_customers.to_csv(
    output_folder / "top_loss_making_customers.csv",
    index=False
)

top_loss_making_products.to_csv(
    output_folder / "top_loss_making_products.csv",
    index=False
)

loss_making_orders_table.to_csv(
    output_folder / "loss_making_orders.csv",
    index=False
)


# ============================================================
# 12. DISPLAY VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("PROFIT & LOSS KPIs")
print("=" * 60)

print(f"Net Profit:         ${net_profit:,.2f}")
print(f"Gross Profit:       ${gross_profit:,.2f}")
print(f"Total Loss:         ${total_loss:,.2f}")
print(f"Loss-Making Orders: {loss_making_orders:,}")

print("\nProfit & Loss analysis completed successfully.")
print("Results saved to analysis_outputs/")