# ============================================================
# SUPERSTORE INTERACTIVE EXECUTIVE DASHBOARD
# DASH + PLOTLY + POSTGRESQL
# ============================================================

import pandas as pd
import plotly.graph_objects as go

from dash import Dash, html, dcc, Input, Output

import db_utils


# ============================================================
# 1. CREATE DASH APP
# ============================================================

app = Dash(__name__)

app.title = "Superstore Executive Dashboard"


# ============================================================
# 2. PROFESSIONAL COLOR SYSTEM
# ============================================================

NAVY = "#1F3864"
BLUE = "#4472C4"
LIGHT_BLUE = "#5B9BD5"

GREEN = "#70AD47"
RED = "#C00000"

ORANGE = "#ED7D31"
TEAL = "#2F75B2"

BACKGROUND = "#F5F7FA"
WHITE = "#FFFFFF"

GRID = "#E5E7EB"
TEXT = "#334155"
MUTED = "#64748B"


# ============================================================
# 3. LOAD DATA FROM POSTGRESQL
# ============================================================

BASE_QUERY = """
SELECT
    o.order_id,
    o.order_date,
    o.region,
    o.state,

    c.customer_name,

    p.category,
    p.sub_category,

    i.sales,
    i.profit

FROM superstore.orders o

JOIN superstore.order_items i
    ON o.order_id = i.order_id

JOIN superstore.customers c
    ON o.customer_id = c.customer_id

JOIN superstore.products p
    ON i.product_key = p.product_key

ORDER BY
    o.order_date;
"""


df = db_utils.run_pg_query(BASE_QUERY)


# ============================================================
# 4. CLEAN DATA
# ============================================================

df["order_date"] = pd.to_datetime(
    df["order_date"],
    errors="coerce"
)

df["sales"] = pd.to_numeric(
    df["sales"],
    errors="coerce"
)

df["profit"] = pd.to_numeric(
    df["profit"],
    errors="coerce"
)


# Remove rows where essential values are missing

df = df.dropna(
    subset=[
        "order_id",
        "order_date",
        "sales",
        "profit"
    ]
).copy()


# ============================================================
# 5. CHECK DATA
# ============================================================

print("\n==============================================")
print("SUPERSTORE DASHBOARD DATA CHECK")
print("==============================================")
print("Rows:", len(df))
print("Columns:", df.columns.tolist())
print("==============================================\n")


# ============================================================
# 6. COMMON CHART LAYOUT
# ============================================================

def base_layout(title, height=430):

    return {

        "title": {
            "text": title,
            "x": 0.02,
            "xanchor": "left",
            "font": {
                "size": 17,
                "color": NAVY
            }
        },

        "template": "plotly_white",

        "height": height,

        "paper_bgcolor": WHITE,

        "plot_bgcolor": WHITE,

        "font": {
            "family": "Arial",
            "color": TEXT
        },

        "margin": {
            "l": 55,
            "r": 45,
            "t": 65,
            "b": 50
        },

        "xaxis": {
            "showgrid": True,
            "gridcolor": GRID
        },

        "yaxis": {
            "showgrid": False
        },

        "hoverlabel": {
            "bgcolor": WHITE,
            "font_size": 12,
            "font_family": "Arial"
        }
    }


# ============================================================
# 7. KPI CARD
# ============================================================

def kpi_card(title, value, accent=BLUE):

    return html.Div(

        [

            html.Div(
                title,
                style={
                    "fontSize": "12px",
                    "fontWeight": "600",
                    "color": MUTED,
                    "textTransform": "uppercase",
                    "letterSpacing": "0.6px"
                }
            ),

            html.Div(
                value,
                style={
                    "fontSize": "27px",
                    "fontWeight": "700",
                    "color": NAVY,
                    "marginTop": "7px"
                }
            )

        ],

        style={

            "backgroundColor": WHITE,

            "borderLeft":
                f"5px solid {accent}",

            "borderRadius": "8px",

            "padding": "17px 20px",

            "boxShadow":
                "0 2px 8px rgba(0,0,0,0.05)"

        }
    )


# ============================================================
# 8. CHART CONTAINER
# ============================================================

def chart_box(figure):

    return html.Div(

        dcc.Graph(

            figure=figure,

            config={
                "displayModeBar": True,
                "responsive": True
            }

        ),

        style={

            "backgroundColor": WHITE,

            "border":
                "1px solid #E5E7EB",

            "borderRadius": "10px",

            "overflow": "hidden"

        }
    )


# ============================================================
# 9. FILTER OPTIONS
# ============================================================

region_options = [

    {
        "label": value,
        "value": value
    }

    for value in sorted(
        df["region"]
        .dropna()
        .unique()
    )

]


category_options = [

    {
        "label": value,
        "value": value
    }

    for value in sorted(
        df["category"]
        .dropna()
        .unique()
    )

]


state_options = [

    {
        "label": value,
        "value": value
    }

    for value in sorted(
        df["state"]
        .dropna()
        .unique()
    )

]


# ============================================================
# 10. SIDEBAR
# ============================================================

sidebar = html.Div(

    [

        html.H2(

            "FILTERS",

            style={
                "color": NAVY,
                "fontSize": "18px",
                "marginBottom": "25px"
            }

        ),


        # ----------------------------------------------------
        # DATE FILTER
        # ----------------------------------------------------

        html.Label(

            "Order Date",

            style={
                "fontWeight": "600",
                "color": TEXT
            }

        ),

        dcc.DatePickerRange(

            id="date-filter",

            min_date_allowed=df[
                "order_date"
            ].min(),

            max_date_allowed=df[
                "order_date"
            ].max(),

            start_date=df[
                "order_date"
            ].min(),

            end_date=df[
                "order_date"
            ].max(),

            display_format="DD MMM YYYY"

        ),


        # ----------------------------------------------------
        # REGION FILTER
        # ----------------------------------------------------

        html.Label(

            "Region",

            style={
                "fontWeight": "600",
                "color": TEXT,
                "display": "block",
                "marginTop": "25px"
            }

        ),

        dcc.Dropdown(

            id="region-filter",

            options=region_options,

            multi=True,

            placeholder="All Regions"

        ),


        # ----------------------------------------------------
        # CATEGORY FILTER
        # ----------------------------------------------------

        html.Label(

            "Category",

            style={
                "fontWeight": "600",
                "color": TEXT,
                "display": "block",
                "marginTop": "25px"
            }

        ),

        dcc.Dropdown(

            id="category-filter",

            options=category_options,

            multi=True,

            placeholder="All Categories"

        ),


        # ----------------------------------------------------
        # STATE FILTER
        # ----------------------------------------------------

        html.Label(

            "State",

            style={
                "fontWeight": "600",
                "color": TEXT,
                "display": "block",
                "marginTop": "25px"
            }

        ),

        dcc.Dropdown(

            id="state-filter",

            options=state_options,

            multi=True,

            placeholder="All States"

        ),


        # ----------------------------------------------------
        # RESET BUTTON
        # ----------------------------------------------------

        html.Button(

            "RESET FILTERS",

            id="reset-button",

            n_clicks=0,

            style={

                "width": "100%",

                "backgroundColor": NAVY,

                "color": WHITE,

                "border": "none",

                "borderRadius": "6px",

                "padding": "11px",

                "marginTop": "25px",

                "fontWeight": "600",

                "cursor": "pointer"

            }

        )

    ],

    style={

        "width": "250px",

        "minWidth": "250px",

        "backgroundColor": WHITE,

        "padding": "25px",

        "boxShadow":
            "2px 0 10px rgba(0,0,0,0.05)",

        "minHeight": "100vh",

        "boxSizing": "border-box"

    }

)


# ============================================================
# 11. MAIN DASHBOARD LAYOUT
# ============================================================

app.layout = html.Div(

    [

        sidebar,


        html.Div(

            [

                # ====================================================
                # HEADER
                # ====================================================

                html.H1(

                    "SUPERSTORE EXECUTIVE BUSINESS PERFORMANCE DASHBOARD",

                    style={
                        "textAlign": "center",
                        "color": NAVY,
                        "fontSize": "27px",
                        "marginBottom": "5px"
                    }

                ),

                html.P(

                    "Interactive analysis of revenue, "
                    "profitability, customers and orders",

                    style={
                        "textAlign": "center",
                        "color": MUTED,
                        "fontSize": "14px",
                        "marginBottom": "25px"
                    }

                ),


                # ====================================================
                # KPI CARDS
                # ====================================================

                html.Div(

                    [

                        html.Div(
                            id="kpi-revenue"
                        ),

                        html.Div(
                            id="kpi-profit"
                        ),

                        html.Div(
                            id="kpi-margin"
                        ),

                        html.Div(
                            id="kpi-orders"
                        )

                    ],

                    style={

                        "display": "grid",

                        "gridTemplateColumns":
                            "repeat(4, 1fr)",

                        "gap": "18px",

                        "marginBottom": "25px"

                    }

                ),


                # ====================================================
                # BUSINESS PERFORMANCE
                # ====================================================

                html.H2(

                    "Business Performance",

                    style={
                        "color": NAVY,
                        "fontSize": "19px"
                    }

                ),


                html.Div(

                    [

                        html.Div(
                            id="monthly-chart"
                        ),

                        html.Div(
                            id="category-profit-chart"
                        )

                    ],

                    style={

                        "display": "grid",

                        "gridTemplateColumns":
                            "repeat(2, 1fr)",

                        "gap": "18px"

                    }

                ),


                # ====================================================
                # CATEGORY PERFORMANCE
                # ====================================================

                html.Div(

                    [

                        html.Div(
                            id="orders-category-chart"
                        ),

                        html.Div(
                            id="furniture-chart"
                        )

                    ],

                    style={

                        "display": "grid",

                        "gridTemplateColumns":
                            "repeat(2, 1fr)",

                        "gap": "18px",

                        "marginTop": "18px"

                    }

                ),


                # ====================================================
                # CUSTOMER PERFORMANCE
                # ====================================================

                html.H2(

                    "Customer Performance",

                    style={
                        "color": NAVY,
                        "fontSize": "19px",
                        "marginTop": "30px"
                    }

                ),


                html.Div(

                    [

                        html.Div(
                            id="revenue-customer-chart"
                        ),

                        html.Div(
                            id="profit-customer-chart"
                        )

                    ],

                    style={

                        "display": "grid",

                        "gridTemplateColumns":
                            "repeat(2, 1fr)",

                        "gap": "18px"

                    }

                ),


                # ====================================================
                # CUSTOMER RISK / ORDERS
                # ====================================================

                html.Div(

                    [

                        html.Div(
                            id="loss-customer-chart"
                        ),

                        html.Div(
                            id="orders-customer-chart"
                        )

                    ],

                    style={

                        "display": "grid",

                        "gridTemplateColumns":
                            "repeat(2, 1fr)",

                        "gap": "18px",

                        "marginTop": "18px"

                    }

                ),


                # ====================================================
                # GEOGRAPHIC PERFORMANCE
                # ====================================================

                html.H2(

                    "Geographic Performance",

                    style={
                        "color": NAVY,
                        "fontSize": "19px",
                        "marginTop": "30px"
                    }

                ),


                html.Div(

                    [

                        html.Div(
                            id="orders-region-chart"
                        ),

                        html.Div(
                            id="orders-state-chart"
                        )

                    ],

                    style={

                        "display": "grid",

                        "gridTemplateColumns":
                            "repeat(2, 1fr)",

                        "gap": "18px"

                    }

                ),


                # ====================================================
                # STATE PROFITABILITY
                # ====================================================

                html.Div(

                    id="state-profit-chart",

                    style={
                        "marginTop": "18px"
                    }

                ),


                # ====================================================
                # FOOTER
                # ====================================================

                html.Hr(

                    style={
                        "marginTop": "40px",
                        "border": "none",
                        "borderTop":
                            "1px solid #E5E7EB"
                    }

                ),

                html.P(

                    "Superstore Business Analytics | "
                    "PostgreSQL • Python • Pandas • Plotly • Dash",

                    style={
                        "textAlign": "center",
                        "color": MUTED,
                        "fontSize": "12px",
                        "paddingBottom": "20px"
                    }

                )

            ],

            style={

                "flex": "1",

                "padding": "30px 40px",

                "minWidth": "0"

            }

        )

    ],

    style={

        "display": "flex",

        "backgroundColor": BACKGROUND,

        "minHeight": "100vh",

        "fontFamily":
            "Arial, sans-serif"

    }

)


# ============================================================
# 12. DASH CALLBACK
# ============================================================

@app.callback(

    Output("kpi-revenue", "children"),
    Output("kpi-profit", "children"),
    Output("kpi-margin", "children"),
    Output("kpi-orders", "children"),

    Output("monthly-chart", "children"),
    Output("category-profit-chart", "children"),

    Output("orders-category-chart", "children"),
    Output("furniture-chart", "children"),

    Output("revenue-customer-chart", "children"),
    Output("profit-customer-chart", "children"),

    Output("loss-customer-chart", "children"),
    Output("orders-customer-chart", "children"),

    Output("orders-region-chart", "children"),
    Output("orders-state-chart", "children"),

    Output("state-profit-chart", "children"),

    Input("date-filter", "start_date"),
    Input("date-filter", "end_date"),

    Input("region-filter", "value"),
    Input("category-filter", "value"),
    Input("state-filter", "value")

)


def update_dashboard(

    start_date,
    end_date,

    selected_regions,
    selected_categories,
    selected_states

):


    # ========================================================
    # 13. FILTER DATA
    # ========================================================

    filtered = df.copy()


    # DATE

    if start_date:

        filtered = filtered[
            filtered["order_date"]
            >= pd.to_datetime(start_date)
        ]


    if end_date:

        end_timestamp = (
            pd.to_datetime(end_date)
            + pd.Timedelta(days=1)
        )

        filtered = filtered[
            filtered["order_date"]
            < end_timestamp
        ]


    # REGION

    if selected_regions:

        filtered = filtered[
            filtered["region"].isin(
                selected_regions
            )
        ]


    # CATEGORY

    if selected_categories:

        filtered = filtered[
            filtered["category"].isin(
                selected_categories
            )
        ]


    # STATE

    if selected_states:

        filtered = filtered[
            filtered["state"].isin(
                selected_states
            )
        ]


    # ========================================================
    # 14. KPI CALCULATIONS
    # ========================================================

    revenue = filtered["sales"].sum()

    profit = filtered["profit"].sum()

    orders = filtered[
        "order_id"
    ].nunique()


    margin = (

        profit / revenue * 100

        if revenue != 0

        else 0

    )


    # ========================================================
    # 15. KPI CARDS
    # ========================================================

    revenue_card = kpi_card(

        "Total Revenue",

        f"${revenue:,.2f}",

        BLUE

    )


    profit_card = kpi_card(

        "Total Profit",

        f"${profit:,.2f}",

        GREEN if profit >= 0 else RED

    )


    margin_card = kpi_card(

        "Profit Margin",

        f"{margin:.2f}%",

        GREEN if margin >= 0 else RED

    )


    orders_card = kpi_card(

        "Total Orders",

        f"{orders:,}",

        TEAL

    )


    # ========================================================
    # 16. MONTHLY REVENUE VS PROFIT
    # ========================================================

    monthly = (

        filtered

        .assign(

            month=
            filtered["order_date"]
            .dt.to_period("M")
            .astype(str)

        )

        .groupby(
            "month",
            as_index=False
        )

        .agg(

            revenue=("sales", "sum"),

            profit=("profit", "sum")

        )

    )


    monthly_fig = go.Figure()


    monthly_fig.add_trace(

        go.Scatter(

            x=monthly["month"],

            y=monthly["revenue"],

            mode="lines+markers",

            name="Revenue",

            line={
                "color": BLUE,
                "width": 2.5
            },

            marker={
                "size": 5
            },

            hovertemplate=
            "<b>%{x}</b>"
            "<br>Revenue: $%{y:,.2f}"
            "<extra></extra>"

        )

    )


    monthly_fig.add_trace(

        go.Scatter(

            x=monthly["month"],

            y=monthly["profit"],

            mode="lines+markers",

            name="Profit",

            line={
                "color": GREEN,
                "width": 2.5
            },

            marker={
                "size": 5
            },

            hovertemplate=
            "<b>%{x}</b>"
            "<br>Profit: $%{y:,.2f}"
            "<extra></extra>"

        )

    )


    monthly_fig.update_layout(

        **base_layout(
            "Monthly Revenue vs Profit",
            430
        ),

        hovermode="x unified",

        legend={
            "orientation": "h",
            "y": 1.08
        }

    )


    # ========================================================
    # 17. PROFIT BY CATEGORY
    # ========================================================

    category = (

        filtered

        .groupby(
            "category",
            as_index=False
        )

        .agg(
            profit=("profit", "sum")
        )

        .sort_values(
            "profit",
            ascending=False
        )

    )


    category_colors = [

        GREEN if value >= 0 else RED

        for value in category["profit"]

    ]


    category_fig = go.Figure(

        go.Bar(

            x=category["category"],

            y=category["profit"],

            text=category["profit"],

            texttemplate="$%{text:,.0f}",

            textposition="outside",

            cliponaxis=False,

            marker_color=category_colors

        )

    )


    category_fig.update_layout(

        **base_layout(
            "Profit by Category",
            430
        )

    )


    # ========================================================
    # 18. ORDERS BY CATEGORY
    # ========================================================

    orders_category = (

        filtered

        .groupby(
            "category"
        )

        .agg(
            orders=
            ("order_id", "nunique")
        )

        .reset_index()

        .sort_values(
            "orders",
            ascending=False
        )

    )


    orders_category_fig = go.Figure(

        go.Bar(

            x=orders_category["category"],

            y=orders_category["orders"],

            text=orders_category["orders"],

            texttemplate="%{text:,}",

            textposition="outside",

            cliponaxis=False,

            marker_color=TEAL

        )

    )


    orders_category_fig.update_layout(

        **base_layout(
            "Orders by Category",
            420
        ),

        yaxis_title="Total Orders"

    )


    # ========================================================
    # 19. FURNITURE PROFIT BY SUB-CATEGORY
    # ========================================================

    furniture = (

        filtered[

            filtered["category"]
            == "Furniture"

        ]

        .groupby(
            "sub_category",
            as_index=False
        )

        .agg(
            profit=("profit", "sum")
        )

        .sort_values(
            "profit",
            ascending=True
        )

    )


    furniture_colors = [

        RED if value < 0 else GREEN

        for value in furniture["profit"]

    ]


    furniture_fig = go.Figure(

        go.Bar(

            x=furniture["sub_category"],

            y=furniture["profit"],

            text=furniture["profit"],

            texttemplate="$%{text:,.0f}",

            textposition="outside",

            cliponaxis=False,

            marker_color=furniture_colors

        )

    )


    furniture_fig.update_layout(

        **base_layout(
            "Furniture Profit by Sub-Category",
            420
        ),

        yaxis_title="Profit ($)"

    )


    # ========================================================
    # 20. TOP 10 CUSTOMERS BY REVENUE
    # ========================================================

    revenue_customers = (

        filtered

        .groupby(
            "customer_name",
            as_index=False
        )

        .agg(
            revenue=("sales", "sum")
        )

        .sort_values(
            "revenue",
            ascending=True
        )

        .tail(10)

    )


    revenue_customer_fig = go.Figure(

        go.Bar(

            x=revenue_customers["revenue"],

            y=revenue_customers[
                "customer_name"
            ],

            orientation="h",

            text=revenue_customers[
                "revenue"
            ],

            texttemplate="$%{text:,.0f}",

            textposition="outside",

            cliponaxis=False,

            marker_color=LIGHT_BLUE

        )

    )


    revenue_customer_fig.update_layout(

        **base_layout(
            "Top 10 Customers by Revenue",
            500
        ),

        xaxis_title="Revenue ($)"

    )


    # ========================================================
    # 21. TOP 10 CUSTOMERS BY PROFIT
    # ========================================================

    profit_customers = (

        filtered

        .groupby(
            "customer_name",
            as_index=False
        )

        .agg(
            profit=("profit", "sum")
        )

        .sort_values(
            "profit",
            ascending=True
        )

        .tail(10)

    )


    profit_customer_fig = go.Figure(

        go.Bar(

            x=profit_customers["profit"],

            y=profit_customers[
                "customer_name"
            ],

            orientation="h",

            text=profit_customers[
                "profit"
            ],

            texttemplate="$%{text:,.0f}",

            textposition="outside",

            cliponaxis=False,

            marker_color=GREEN

        )

    )


    profit_customer_fig.update_layout(

        **base_layout(
            "Top 10 Customers by Profit",
            500
        ),

        xaxis_title="Profit ($)"

    )


    # ========================================================
    # 22. TOP 10 LOSS-MAKING CUSTOMERS
    # ========================================================

    loss_customers = (

        filtered

        .groupby(
            "customer_name",
            as_index=False
        )

        .agg(
            profit=("profit", "sum")
        )

    )


    loss_customers = (

        loss_customers[

            loss_customers["profit"] < 0

        ]

        .sort_values(
            "profit",
            ascending=True
        )

        .head(10)

    )


    loss_customer_fig = go.Figure(

        go.Bar(

            x=loss_customers["profit"],

            y=loss_customers[
                "customer_name"
            ],

            orientation="h",

            text=loss_customers[
                "profit"
            ],

            texttemplate="$%{text:,.0f}",

            textposition="outside",

            cliponaxis=False,

            marker_color=RED

        )

    )


    # IMPORTANT:
    # We do NOT pass xaxis twice to update_layout.
    # base_layout already contains xaxis.

    loss_customer_fig.update_layout(

        **base_layout(
            "Top 10 Loss-Making Customers",
            500
        ),

        xaxis_title="Profit ($)"

    )


    loss_customer_fig.update_xaxes(

        zeroline=True,

        zerolinecolor=GRID,

        zerolinewidth=1

    )


    # ========================================================
    # 23. TOP 10 CUSTOMERS BY ORDERS
    # ========================================================

    orders_customer = (

        filtered

        .groupby(
            "customer_name",
            as_index=False
        )

        .agg(
            orders=
            ("order_id", "nunique")
        )

        .sort_values(
            "orders",
            ascending=True
        )

        .tail(10)

    )


    orders_customer_fig = go.Figure(

        go.Bar(

            x=orders_customer["orders"],

            y=orders_customer[
                "customer_name"
            ],

            orientation="h",

            text=orders_customer[
                "orders"
            ],

            texttemplate="%{text:,}",

            textposition="outside",

            cliponaxis=False,

            marker_color=BLUE

        )

    )


    orders_customer_fig.update_layout(

        **base_layout(
            "Top 10 Customers by Orders",
            500
        ),

        xaxis_title="Total Orders"

    )


    # ========================================================
    # 24. ORDERS BY REGION
    # ========================================================

    orders_region = (

        filtered

        .groupby(
            "region",
            as_index=False
        )

        .agg(
            orders=
            ("order_id", "nunique")
        )

        .sort_values(
            "orders",
            ascending=False
        )

    )


    orders_region_fig = go.Figure(

        go.Bar(

            x=orders_region["region"],

            y=orders_region["orders"],

            text=orders_region["orders"],

            texttemplate="%{text:,}",

            textposition="outside",

            cliponaxis=False,

            marker_color=ORANGE

        )

    )


    orders_region_fig.update_layout(

        **base_layout(
            "Orders by Region",
            430
        ),

        yaxis_title="Total Orders"

    )


    # ========================================================
    # 25. ORDERS BY STATE
    # ========================================================

    orders_state = (

        filtered

        .groupby(
            "state",
            as_index=False
        )

        .agg(
            orders=
            ("order_id", "nunique")
        )

        .sort_values(
            "orders",
            ascending=True
        )

        .tail(10)

    )


    orders_state_fig = go.Figure(

        go.Bar(

            x=orders_state["orders"],

            y=orders_state["state"],

            orientation="h",

            text=orders_state["orders"],

            texttemplate="%{text:,}",

            textposition="outside",

            cliponaxis=False,

            marker_color=TEAL

        )

    )


    orders_state_fig.update_layout(

        **base_layout(
            "Top 10 States by Orders",
            550
        ),

        xaxis_title="Total Orders"

    )


    # ========================================================
    # 26. STATE PROFITABILITY
    # ========================================================

    state_profit = (

        filtered

        .groupby(
            "state",
            as_index=False
        )

        .agg(
            profit=("profit", "sum")
        )

    )


    state_profit_sorted = (

        state_profit

        .sort_values(
            "profit",
            ascending=True
        )

    )


    bottom_5 = (
        state_profit_sorted
        .head(5)
    )


    top_5 = (
        state_profit_sorted
        .tail(5)
    )


    state_plot = (

        pd.concat(
            [
                bottom_5,
                top_5
            ]
        )

        .drop_duplicates()

        .sort_values(
            "profit",
            ascending=True
        )

    )


    state_colors = [

        RED if value < 0 else GREEN

        for value in state_plot["profit"]

    ]


    state_fig = go.Figure(

        go.Bar(

            x=state_plot["profit"],

            y=state_plot["state"],

            orientation="h",

            text=state_plot["profit"],

            texttemplate="$%{text:,.0f}",

            textposition="outside",

            cliponaxis=False,

            marker_color=state_colors

        )

    )


    # IMPORTANT:
    # Same fix as the loss-customer chart.
    # xaxis is not supplied twice.

    state_fig.update_layout(

        **base_layout(
            "State Profitability — Top 5 & Bottom 5",
            650
        ),

        xaxis_title="Profit ($)"

    )


    state_fig.update_xaxes(

        zeroline=True,

        zerolinecolor=GRID,

        zerolinewidth=1

    )


    # ========================================================
    # 27. RETURN DASHBOARD COMPONENTS
    # ========================================================

    return (

        revenue_card,

        profit_card,

        margin_card,

        orders_card,

        chart_box(
            monthly_fig
        ),

        chart_box(
            category_fig
        ),

        chart_box(
            orders_category_fig
        ),

        chart_box(
            furniture_fig
        ),

        chart_box(
            revenue_customer_fig
        ),

        chart_box(
            profit_customer_fig
        ),

        chart_box(
            loss_customer_fig
        ),

        chart_box(
            orders_customer_fig
        ),

        chart_box(
            orders_region_fig
        ),

        chart_box(
            orders_state_fig
        ),

        chart_box(
            state_fig
        )

    )


# ============================================================
# 28. RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    
    app.run(
        debug=True,
        host="0.0.0.0",
        port=8050
    )