-- 1. Create Raw Data Table (Mock Schema)
CREATE TABLE raw_transactions (
    transaction_id VARCHAR(50),
    transaction_date TIMESTAMP,
    amount DECIMAL(10, 2),
    payment_method VARCHAR(50),
    gateway VARCHAR(50),
    status VARCHAR(20), -- 'Success' or 'Failed'
    error_code VARCHAR(50)
);

-- 2. Data Cleaning & Transformation
-- Handling NULLs, standardizing text, and casting data types
CREATE TABLE cleaned_transactions AS
SELECT 
    transaction_id,
    DATE(transaction_date) AS transaction_date,
    HOUR(transaction_date) AS transaction_hour,
    amount,
    UPPER(TRIM(payment_method)) AS payment_method,
    UPPER(TRIM(gateway)) AS gateway,
    status,
    CASE 
        WHEN status = 'Failed' AND error_code IS NULL THEN 'Unknown Error'
        ELSE COALESCE(error_code, 'No Error')
    END AS error_code
FROM raw_transactions
WHERE transaction_id IS NOT NULL 
  AND amount > 0;

-- 3. Aggregation: Success/Failure Rates by Gateway
CREATE VIEW gateway_performance AS
SELECT 
    gateway,
    COUNT(transaction_id) AS total_transactions,
    SUM(CASE WHEN status = 'Success' THEN 1 ELSE 0 END) AS successful_transactions,
    SUM(CASE WHEN status = 'Failed' THEN 1 ELSE 0 END) AS failed_transactions,
    ROUND((SUM(CASE WHEN status = 'Failed' THEN 1 ELSE 0 END) * 100.0 / COUNT(transaction_id)), 2) AS failure_rate_pct
FROM cleaned_transactions
GROUP BY gateway
ORDER BY failure_rate_pct DESC;

-- 4. Aggregation: Failure Reasons by Payment Method (For Power BI)
CREATE VIEW failure_analysis AS
SELECT 
    payment_method,
    error_code,
    COUNT(transaction_id) AS failure_count
FROM cleaned_transactions
WHERE status = 'Failed'
GROUP BY payment_method, error_code
ORDER BY payment_method, failure_count DESC;
