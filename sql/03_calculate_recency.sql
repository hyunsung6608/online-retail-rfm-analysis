-- Recency 계산

WITH clean_data AS (
    SELECT *
    FROM online_retail
    WHERE CustomerID IS NOT NULL    -- 고객 ID 없는 데이터 제거
      AND Quantity > 0              -- 반품 제거
      AND UnitPrice > 0             -- 가격 이상치 제거
),

snapshot AS (
    SELECT DATE_ADD(MAX(InvoiceDate), INTERVAL 1 DAY) AS snapshot_date
    FROM clean_data
)

SELECT
    c.CustomerID,
    DATEDIFF(MAX(s.snapshot_date), MAX(c.InvoiceDate)) AS Recency
FROM clean_data c
CROSS JOIN snapshot s
GROUP BY c.CustomerID
ORDER BY Recency ASC;