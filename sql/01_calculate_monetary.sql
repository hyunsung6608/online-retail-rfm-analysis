-- Monetary 계산

WITH clean_data AS (
    SELECT *
    FROM online_retail
    WHERE CustomerID IS NOT NULL    -- 고객 ID 없는 데이터 제거
      AND Quantity > 0              -- 반품 제거
      AND UnitPrice > 0             -- 가격 이상치 제거
)

SELECT 
    CustomerID,
    SUM(Quantity * UnitPrice) AS Monetary
FROM clean_data
GROUP BY CustomerID
ORDER BY Monetary DESC;