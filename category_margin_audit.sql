-- Category & Sub-Category Profitability & Discount Audit
SELECT 
    p.category,
    p.sub_category,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(o.sales), 2) AS total_revenue,
    ROUND(SUM(o.profit), 2) AS total_profit,
    ROUND((SUM(o.profit) / SUM(o.sales)) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(o.discount) * 100, 2) AS avg_discount_pct
FROM superstore.orders o
JOIN superstore.products p ON o.product_id = p.product_id
GROUP BY p.category, p.sub_category
ORDER BY total_profit ASC;