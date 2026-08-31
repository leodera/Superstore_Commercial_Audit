-- Executive Audit: Global KPIs & Baseline Reconciliation
SELECT 
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(row_id) AS total_line_items,
    COUNT(DISTINCT customer_id) AS total_customers,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_net_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS overall_profit_margin_pct
FROM superstore.orders;