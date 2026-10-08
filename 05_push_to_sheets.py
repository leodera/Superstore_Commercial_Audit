# ============================================================
# SUPERSTORE COMMERCIAL AUDIT
# 05 - PUSH ANALYSIS RESULTS TO GOOGLE SHEETS
# ============================================================

import gspread
import pandas as pd

from pathlib import Path
from google.oauth2.service_account import Credentials


# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = BASE_DIR / "analysis_outputs"

CREDENTIALS_FILE = BASE_DIR / "credentials.json"


# ============================================================
# 2. GOOGLE SHEETS CONNECTION
# ============================================================

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_file(
    CREDENTIALS_FILE,
    scopes=SCOPES
)

gc = gspread.authorize(credentials)

print("Connected to Google Sheets!")


# ============================================================
# 3. OPEN SPREADSHEET
# ============================================================

spreadsheet = gc.open("sup")

print(
    f"Spreadsheet opened: {spreadsheet.title}"
)


# ============================================================
# 4. REUSABLE DATAFRAME → GOOGLE SHEETS FUNCTION
# ============================================================

def push_dataframe_to_sheet(df, worksheet_name):
    """
    Push a pandas DataFrame into a Google Sheets worksheet.

    If the worksheet does not exist, it is created.

    If the worksheet already exists, its old contents
    are cleared before the new data is written.
    """

    # --------------------------------------------------------
    # Find or create worksheet
    # --------------------------------------------------------

    try:

        worksheet = spreadsheet.worksheet(
            worksheet_name
        )

        print(
            f"Found existing worksheet: "
            f"{worksheet_name}"
        )

    except gspread.WorksheetNotFound:

        worksheet = spreadsheet.add_worksheet(
            title=worksheet_name,
            rows=1000,
            cols=30
        )

        print(
            f"Created new worksheet: "
            f"{worksheet_name}"
        )


    # --------------------------------------------------------
    # Clear previous data
    # --------------------------------------------------------

    worksheet.clear()


    # --------------------------------------------------------
    # Prepare data
    # --------------------------------------------------------

    data = [
        df.columns.tolist()
    ] + df.astype(object).values.tolist()


    # --------------------------------------------------------
    # Clean values before uploading
    # --------------------------------------------------------

    cleaned_data = []

    for row in data:

        cleaned_row = []

        for value in row:

            if pd.isna(value):

                cleaned_row.append("")

            elif isinstance(value, pd.Timestamp):

                cleaned_row.append(
                    value.strftime("%Y-%m-%d")
                )

            else:

                cleaned_row.append(value)

        cleaned_data.append(cleaned_row)


    # --------------------------------------------------------
    # Upload
    # --------------------------------------------------------

    worksheet.update(
        range_name="A1",
        values=cleaned_data
    )


    print(
        f"Uploaded {len(df):,} rows "
        f"to '{worksheet_name}'"
    )


# ============================================================
# 5. HELPER FUNCTION TO LOAD CSV
# ============================================================

def load_output(filename):
    """
    Load a CSV file from the analysis_outputs folder.
    """

    file_path = OUTPUT_DIR / filename

    if not file_path.exists():

        raise FileNotFoundError(
            f"Required analysis file not found: "
            f"{file_path}"
        )

    return pd.read_csv(file_path)


# ============================================================
# 6. EXECUTIVE ANALYSIS OUTPUTS
# ============================================================

executive_kpis = load_output(
    "executive_kpis.csv"
)

sales_by_category = load_output(
    "sales_by_category.csv"
)

sales_by_region = load_output(
    "sales_by_region.csv"
)

sales_by_segment = load_output(
    "sales_by_segment.csv"
)

monthly_sales_profit = load_output(
    "monthly_sales_profit.csv"
)


# ============================================================
# 7. PROFIT & LOSS OUTPUTS
# ============================================================

profit_loss_kpis = load_output(
    "profit_loss_kpis.csv"
)

profit_by_category = load_output(
    "profit_by_category.csv"
)

profit_by_subcategory = load_output(
    "profit_by_subcategory.csv"
)

loss_by_region = load_output(
    "loss_by_region.csv"
)

loss_by_segment = load_output(
    "loss_by_segment.csv"
)

top_loss_making_customers = load_output(
    "top_loss_making_customers.csv"
)

top_loss_making_products = load_output(
    "top_loss_making_products.csv"
)

loss_making_orders = load_output(
    "loss_making_orders.csv"
)


# ============================================================
# 8. DISCOUNT ANALYSIS OUTPUT
# ============================================================

discount_impact = load_output(
    "discount_impact_analysis.csv"
)


# ============================================================
# 9. PUSH EXECUTIVE OUTPUTS
# ============================================================

push_dataframe_to_sheet(
    executive_kpis,
    "Executive KPIs"
)

push_dataframe_to_sheet(
    sales_by_category,
    "Sales by Category"
)

push_dataframe_to_sheet(
    sales_by_region,
    "Sales by Region"
)

push_dataframe_to_sheet(
    sales_by_segment,
    "Sales by Segment"
)

push_dataframe_to_sheet(
    monthly_sales_profit,
    "Monthly Sales Profit"
)


# ============================================================
# 10. PUSH PROFIT & LOSS OUTPUTS
# ============================================================

push_dataframe_to_sheet(
    profit_loss_kpis,
    "Profit Loss KPIs"
)

push_dataframe_to_sheet(
    profit_by_category,
    "Profit by Category"
)

push_dataframe_to_sheet(
    profit_by_subcategory,
    "Profit by Subcategory"
)

push_dataframe_to_sheet(
    loss_by_region,
    "Loss by Region"
)

push_dataframe_to_sheet(
    loss_by_segment,
    "Loss by Segment"
)

push_dataframe_to_sheet(
    top_loss_making_customers,
    "Top Loss Customers"
)

push_dataframe_to_sheet(
    top_loss_making_products,
    "Top Loss Products"
)

push_dataframe_to_sheet(
    loss_making_orders,
    "Loss Making Orders"
)


# ============================================================
# 11. PUSH DISCOUNT OUTPUT
# ============================================================

push_dataframe_to_sheet(
    discount_impact,
    "Discount Impact"
)


# ============================================================
# 12. COMPLETE
# ============================================================

print("\n" + "=" * 60)
print("ALL ANALYSIS RESULTS PUSHED TO GOOGLE SHEETS")
print("=" * 60)