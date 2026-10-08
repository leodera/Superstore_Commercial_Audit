# ============================================================
# SUPERSTORE COMMERCIAL AUDIT
# 04 - DISCOUNT IMPACT ANALYSIS
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
# 3. CREATE DISCOUNT BANDS
# ============================================================

def create_discount_band(discount):

    if discount == 0:
        return "0% - No Discount"

    elif discount <= 0.10:
        return "1-10%"

    elif discount <= 0.20:
        return "11-20%"

    elif discount <= 0.30:
        return "21-30%"

    else:
        return "31%+"


df["discount_band"] = df["discount"].apply(
    create_discount_band
)


# ============================================================
# 4. SET CORRECT BAND ORDER
# ============================================================

discount_order = [
    "0% - No Discount",
    "1-10%",
    "11-20%",
    "21-30%",
    "31%+"
]

df["discount_band"] = pd.Categorical(
    df["discount_band"],
    categories=discount_order,
    ordered=True
)


# ============================================================
# 5. ANALYSE DISCOUNT BANDS
# ============================================================

discount_analysis = (
    df.groupby(
        "discount_band",
        observed=True,
        as_index=False
    )
    .agg(
        sales=("sales", "sum"),
        profit=("profit", "sum"),
        quantity=("quantity", "sum"),
        orders=("order_id", "nunique")
    )
)


# ============================================================
# 6. CALCULATE PROFIT MARGIN
# ============================================================

discount_analysis["profit_margin"] = (
    discount_analysis["profit"]
    / discount_analysis["sales"]
)


# ============================================================
# 7. CALCULATE AVERAGE DISCOUNT
# ============================================================

average_discount_by_band = (
    df.groupby(
        "discount_band",
        observed=True
    )["discount"]
    .mean()
    .reset_index(name="average_discount")
)

discount_analysis = discount_analysis.merge(
    average_discount_by_band,
    on="discount_band"
)


# ============================================================
# 8. OVERALL METRICS
# ============================================================

total_sales = df["sales"].sum()

total_profit = df["profit"].sum()

average_discount = df["discount"].mean()

overall_profit_margin = total_profit / total_sales


# ============================================================
# 9. DISPLAY RESULTS
# ============================================================

print("\n" + "=" * 60)
print("DISCOUNT IMPACT ANALYSIS")
print("=" * 60)

print(
    discount_analysis[
        [
            "discount_band",
            "sales",
            "profit",
            "profit_margin",
            "quantity",
            "orders",
            "average_discount"
        ]
    ]
)


print("\n" + "=" * 60)
print("OVERALL DISCOUNT METRICS")
print("=" * 60)

print(f"Average Discount:      {average_discount:.2%}")
print(f"Overall Profit Margin: {overall_profit_margin:.2%}")


# ============================================================
# 10. IDENTIFY FIRST NEGATIVE-MARGIN BAND
# ============================================================

negative_margin_bands = discount_analysis[
    discount_analysis["profit_margin"] < 0
]

if not negative_margin_bands.empty:

    first_negative_band = (
        negative_margin_bands.iloc[0]["discount_band"]
    )

    print(
        "\nProfit margin first becomes negative at:"
    )

    print(first_negative_band)

else:

    print(
        "\nNo discount band has negative profit margin."
    )


# ============================================================
# 11. SAVE OUTPUT
# ============================================================

discount_analysis.to_csv(
    output_folder / "discount_impact_analysis.csv",
    index=False
)


# ============================================================
# 12. FINAL MESSAGE
# ============================================================

print("\nDiscount impact analysis completed successfully.")
print("Results saved to analysis_outputs/")