DROP TABLE IF EXISTS rfm;

CREATE TABLE rfm AS
WITH clean_data AS (
    SELECT *
    FROM online_retail
    WHERE CustomerID IS NOT NULL    -- 고객 ID 없는 데이터 제거
      AND Quantity > 0              -- 반품 제거
      AND UnitPrice > 0             -- 가격 이상치 제거
),

-- 기준 날짜 설정
snapshot AS (
    SELECT DATE_ADD(MAX(InvoiceDate), INTERVAL 1 DAY) AS snapshot_date
    FROM clean_data
)

SELECT
    c.CustomerID,
    DATEDIFF(MAX(s.snapshot_date), MAX(c.InvoiceDate)) AS Recency,   -- 최근 구매일로부터 현재까지 경과일
    COUNT(DISTINCT c.InvoiceNo) AS Frequency,   -- 구매 횟수
    SUM(c.Quantity * c.UnitPrice) AS Monetary   -- 총 구매 금액
FROM clean_data c
CROSS JOIN snapshot s
GROUP BY c.CustomerID;

ALTER TABLE rfm
ADD PRIMARY KEY (CustomerID);

SELECT * FROM rfm LIMIT 10;