-- Unprofitable Customer Accounts & Outlier Loss Leader Ranking
WITH customer_summary AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        c.segment,
        COUNT(DISTINCT o.order_id) AS total_orders,
        ROUND(SUM(o.sales), 2) AS total_revenue,
        ROUND(SUM(o.profit), 2) AS net_profit,
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
FROM customer_summary
WHERE net_profit < 0
ORDER BY net_profit ASC;