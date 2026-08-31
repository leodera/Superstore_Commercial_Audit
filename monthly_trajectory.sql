-- Monthly Revenue & Profit Margin Trajectory (48-Month Trend)
SELECT 
    TO_CHAR(order_date, 'YYYY-MM') AS year_month,
    COUNT(DISTINCT order_id) AS monthly_orders,
    ROUND(SUM(sales), 2) AS monthly_revenue,
    ROUND(SUM(profit), 2) AS monthly_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS monthly_margin_pct
FROM superstore.orders
GROUP BY TO_CHAR(order_date, 'YYYY-MM')
ORDER BY year_month ASC;