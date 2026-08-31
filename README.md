# Superstore Commercial Performance & Margin Audit

An end-to-end commercial audit evaluating discount elasticity, sub-category profitability, and enterprise customer risk across 9,994 retail transactions ($2.30M in revenue).

---

## Executive Summary & Core Findings

* **Enterprise Health:** Total revenue reached **$2,296,919.49** with a net profit of **$286,409.08**, delivering an aggregate profit margin of **12.47%** across **5,009 unique orders**.
* **Core Profit Drivers:** **Technology** ($145.5K profit, 17.4% margin) and **Office Supplies** ($122.5K profit, 17.0% margin) generated **93.5%** of net commercial profit.
* **Structural Furniture Erosion:** The Furniture category delivered a margin of only **2.5%** ($18.5K profit on $742.0K sales), driven by severe negative returns in **Tables (-$17.7K net loss, -8.6% margin)** and **Bookcases (-$3.5K net loss, -3.0% margin)**.
* **Discount Cliff Threshold:** Margin collapse accelerates once discounts exceed **20%**. Transactions discounted between 21%–40% saw margins plummet to **-14.3%**, and discounts >60% destroyed capital at **-83.6% margin**.
* **Account Risk Concentration:** Exactly **155 out of 793 customers (19.5%)** are net unprofitable on a lifetime basis, driving **-$71,200** in cumulative capital destruction due to unmanaged high-ticket enterprise discounts.

---

## Tech Stack & Data Architecture

* **Database & Modeling:** PostgreSQL (Supabase Cloud), Star Schema (`orders`, `customers`, `products`), DBeaver.
* **Spreadsheet Audit & Reconciliation:** Google Sheets (Dynamic Array Formulas, `LET/LAMBDA`, `SUMIF`, Pivot Tables).
* **Business Intelligence & Reporting:** Google Looker Studio (Direct live PostgreSQL connection, interactive cross-filtering, custom calculated metrics).

---

## Dimensional Data Model (Star Schema)

```
       superstore.customers                      superstore.products
       ┌─────────────────────────┐               ┌─────────────────────────┐
       │ customer_id (PK)        │               │ product_id (PK)         │
       │ customer_name           │               │ category                │
       │ segment                 │               │ sub_category            │
       └────────────┬────────────┘               │ product_name            │
                    │                            └────────────┬────────────┘
                    │ 1                                       │ 1
                    │                                         │
                    └───────────────┐         ┌───────────────┘
                                    │         │
                                  * │         │ *
                              ┌─────┴─────────┴─────┐
                              │ superstore.orders   │
                              ├─────────────────────┤
                              │ row_id (PK)         │
                              │ order_id            │
                              │ order_date          │
                              │ ship_date           │
                              │ ship_mode           │
                              │ customer_id (FK)    │
                              │ product_id (FK)     │
                              │ sales               │
                              │ quantity            │
                              │ discount            │
                              │ profit              │
                              └─────────────────────┘

```

---

## Key SQL Queries & Audit Scripts

### 1. Customer Net Profitability & Outlier Identification

```sql
WITH customer_performance AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        c.segment,
        COUNT(DISTINCT o.order_id) AS total_orders,
        SUM(o.sales) AS total_revenue,
        SUM(o.profit) AS net_profit,
        ROUND((SUM(o.profit) / SUM(o.sales)) * 100, 2) AS profit_margin_pct,
        ROUND(AVG(o.discount) * 100, 2) AS avg_discount_pct
    FROM superstore.orders o
    JOIN superstore.customers c ON o.customer_id = c.customer_id
    GROUP BY c.customer_id, c.customer_name, c.segment
)
SELECT 
    customer_id,
    customer_name,
    segment,
    total_orders,
    total_revenue,
    net_profit,
    profit_margin_pct,
    avg_discount_pct,
    RANK() OVER (ORDER BY net_profit ASC) AS loss_rank
FROM customer_performance
WHERE net_profit < 0
ORDER BY net_profit ASC;

```

### 2. Discount Elasticity & Margin Degradation Tiers

```sql
SELECT 
    CASE 
        WHEN discount = 0 THEN '1. No Discount (0%)'
        WHEN discount <= 0.20 THEN '2. Low (1% - 20%)'
        WHEN discount <= 0.40 THEN '3. Moderate (21% - 40%)'
        WHEN discount <= 0.60 THEN '4. Heavy (41% - 60%)'
        ELSE '5. Deep (>60%)'
    END AS discount_tier,
    COUNT(row_id) AS transaction_count,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct
FROM superstore.orders
GROUP BY 1
ORDER BY 1;

```

---

## Strategic Recommendations

1. **Category Policy Restructuring:**
* Enforce a hard **0% discount ceiling on Tables** and a strict **20% maximum discount on Bookcases**.
* Re-evaluate supplier procurement costs and freight distribution rates for heavy furniture SKUs.


2. **Enterprise Discount Governance:**
* Mandate Director-level sign-off for any commercial quote with discounts $>20\%$ on orders above $1,000.
* Restrict non-standard pricing for repeat negative-margin accounts (e.g., Cindy Stewart, Grant Thornton, Luke Foster).


3. **Product Bundling Strategy:**
* Require loss-making furniture SKUs to be bundled with high-margin Technology (17.4%) or Office Supply (17.0%) accessories to safeguard order-level margins.



---

## Interactive BI Dashboard

* **Live Dashboard URL:** https://datastudio.google.com/reporting/f57f1448-dc94-4fb0-9104-8c5b2ad731d2
* **Database Host:** Supabase Cloud PostgreSQL
