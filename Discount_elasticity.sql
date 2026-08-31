-- Discount Tier Elasticity & Margin Degradation Analysis
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