-- 1. Top 5 funds by AUM

SELECT
scheme_name,
aum_crore
FROM fact_performance
ORDER BY aum_crore DESC
LIMIT 5;



-- 2. Average NAV

SELECT
AVG(nav) AS average_nav
FROM fact_nav;



-- 3. SIP transaction count

SELECT
COUNT(*) AS sip_count
FROM fact_transactions
WHERE transaction_type='SIP';



-- 4. Transactions by state

SELECT
state,
COUNT(*) AS total_transactions
FROM fact_transactions
GROUP BY state
ORDER BY total_transactions DESC;



-- 5. Funds with expense ratio below 1%

SELECT
scheme_name,
expense_ratio_pct
FROM fact_performance
WHERE expense_ratio_pct < 1;



-- 6. Highest 5 year return funds

SELECT
scheme_name,
return_5yr_pct
FROM fact_performance
ORDER BY return_5yr_pct DESC
LIMIT 5;



-- 7. Total investment amount

SELECT
SUM(amount_inr) AS total_amount
FROM fact_transactions;



-- 8. Redemption transactions

SELECT
SUM(amount_inr) AS redemption_amount
FROM fact_transactions
WHERE transaction_type='REDEMPTION';



-- 9. Transactions by payment mode

SELECT
payment_mode,
COUNT(*) AS total
FROM fact_transactions
GROUP BY payment_mode;



-- 10. Average expense ratio

SELECT
AVG(expense_ratio_pct)
FROM fact_performance;