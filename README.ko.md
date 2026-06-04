# Online Retail RFM 분석

## 1. 프로젝트 개요

고객 가치는 균등하게 분포하지 않습니다.
소수의 고가치 고객이 매출의 대부분을 만들어내는 경우가 많지만,
세그멘테이션 없이는 이들이 일반 고객과 동일하게 취급됩니다.

이 프로젝트는 RFM(Recency, Frequency, Monetary) 분석을 통해
고객의 구매 행동 기반 세그멘테이션을 수행합니다.
원시 트랜잭션 데이터에서 시작해 Tableau 인터랙티브 대시보드까지
end-to-end 파이프라인으로 구현했습니다.

**핵심 포인트:** 전체 고객의 단 8.02%가 VIP로 분류되었지만,
총 매출의 43.82%를 차지했습니다 — 강한 파레토 분포 확인.

## 2. 핵심 성과

- **397,884건** 트랜잭션 처리 및 **4,338명** 고객 분석
- VIP 세그먼트 (**8.02%**) 가 총 매출의 **43.82%** 기여 — 강한 파레토 분포 확인
- Python 정제 → MySQL 데이터마트 → Tableau 대시보드 end-to-end 파이프라인 구축
- 데이터마트 구성 전 각 RFM 지표를 SQL로 독립 검증

## 3. 프로젝트 흐름

원시 CSV → Python 데이터 정제 & 탐색 분석 → MySQL 적재 → SQL 기반 변환 & 검증 → RFM 데이터마트 구축 → Python/Tableau 시각화

## 4. 데이터 모델 & 데이터마트 설계

![데이터 모델 ERD](images/data_model_erd.png)

이 프로젝트는 트랜잭션 데이터와 분석용 고객 단위 데이터마트를 명확히 분리하여 설계했습니다.

트랜잭션 단위 데이터(`online_retail`)는 고객 단위 RFM 지표로 변환·집계되어 `rfm` 테이블에 저장됩니다.

이 구조는 효율적인 고객 세그멘테이션을 가능하게 하고, 확장 가능하고 재현 가능한 분석 워크플로우를 지원합니다.

### 데이터 모델 개요

두 가지 주요 레이어로 구성됩니다:

- **트랜잭션 단위 테이블 (`online_retail`)**
  - MySQL에 적재된 정제 트랜잭션 데이터 저장
  - `InvoiceNo`, `StockCode`, `Quantity`, `UnitPrice`, `CustomerID`, `InvoiceDate` 등 포함

- **고객 단위 데이터마트 (`rfm`)**
  - 트랜잭션 데이터에서 파생된 집계 테이블
  - 고객당 1행
  - 세그멘테이션 및 분석을 위한 RFM 지표 저장

### 데이터마트 설계

고객 행동 분석을 지원하는 고객 중심 데이터마트를 설계했습니다.

- `rfm` 테이블은 **주제 지향적 분석 테이블**로 활용
- SQL 집계를 통해 트랜잭션 데이터를 고객 단위 지표로 변환
- 분석 쿼리, 시각화, 비즈니스 인사이트에 최적화된 구조

### 데이터 변환 로직

원시 데이터에서 데이터마트까지의 변환 과정:

- 데이터 검증:
  - `CustomerID` 누락 행 제거
  - 반품 트랜잭션 제외 (`Quantity <= 0`)
  - 유효하지 않은 가격 레코드 필터링 (`UnitPrice <= 0`)
- 피처 엔지니어링:
  - `Sales = Quantity × UnitPrice`
- 집계:
  - **Recency**: 마지막 구매 이후 경과 일수
  - **Frequency**: 고객별 주문 수
  - **Monetary**: 고객별 총 구매 금액

### 설계 근거

- 원시 데이터는 추적 가능성을 위해 트랜잭션 단위로 보존
- 집계 데이터는 성능과 명확성을 위해 별도 분석 테이블로 분리
- SQL 기반 변환으로 분석 결과의 재현성과 일관성 보장
- 데이터마트 구조는 확장 가능한 고객 세그멘테이션과 후속 분석을 지원

## 5. 프로젝트 요약

- Python과 MySQL을 결합한 end-to-end 데이터 파이프라인 구축
- Python으로 데이터 정제, SQL로 검증 및 집계 수행
- 고객 단위 RFM 데이터마트 설계 및 구축
- RFM 분석을 통한 구매 행동 기반 고객 세그멘테이션
- 고가치 고객 그룹 식별 및 비즈니스 인사이트 도출

## 6. 기술 스택

- **언어**: Python, SQL
- **데이터 처리**: Pandas, NumPy
- **데이터베이스**: MySQL
- **ORM / 연결**: SQLAlchemy, PyMySQL
- **시각화**: Matplotlib, Tableau
- **환경 관리**: python-dotenv
- **노트북**: Jupyter Notebook
- **개발 환경**: VS Code
- **주요 개념**: 데이터 정제, 데이터 변환, 데이터 검증, 데이터마트 설계

## 7. 데이터셋

이 프로젝트는 영국 기반 온라인 리테일 기업의 트랜잭션 기록을 담은 Online Retail 데이터셋을 사용합니다.

고객 행동 분석 및 RFM 기반 세그멘테이션에 적합한 트랜잭션 단위 구매 이력을 포함합니다.

주요 컬럼:
- `InvoiceNo`: 주문 식별자
- `StockCode`: 상품 코드
- `Description`: 상품명
- `Quantity`: 구매 수량
- `InvoiceDate`: 트랜잭션 타임스탬프
- `UnitPrice`: 단가
- `CustomerID`: 고객 식별자
- `Country`: 고객 국가

고객 단위 분석 데이터마트 구축에 필요한 구매 최근성, 주문 빈도, 총 구매 금액 계산이 가능한 데이터셋입니다.

## 8. 데이터 처리 파이프라인

원시 데이터 수집부터 분석용 데이터마트 구축까지의 end-to-end 파이프라인:

1. CSV에서 원시 트랜잭션 데이터 로드
2. Python으로 데이터 정제 및 검증
3. `Sales` 파생 컬럼 생성 (`Quantity * UnitPrice`)
4. 정제 데이터셋을 MySQL에 적재
5. SQL 기반 변환 및 지표 검증
6. 트랜잭션 데이터를 고객 단위 RFM 데이터마트(`rfm`)로 집계
7. Python 및 Tableau에서 분석, 세그멘테이션, 시각화

## 9. 데이터 전처리 & 변환

데이터 품질과 분석 일관성을 보장하기 위해 Python과 SQL 두 단계로 처리했습니다.

### Python (데이터 정제)

MySQL 적재 전 원시 데이터셋을 정제했습니다.

- `InvoiceDate`를 datetime 형식으로 변환
- `CustomerID` 누락 행 제거
- 반품 트랜잭션 제외 (`Quantity <= 0`)
- 유효하지 않은 가격 레코드 제거 (`UnitPrice <= 0`)
- `CustomerID`를 정수형으로 변환
- `Sales` 컬럼 생성 (`Quantity * UnitPrice`)

전처리 로직: `scripts/preprocess_and_load.py`

MySQL 적재 후 정제된 데이터셋이 로드됩니다.

### SQL (데이터 검증 & 집계)

SQL로 지표를 검증하고 분석 데이터셋을 구축했습니다.

- CTE(`clean_data`)를 사용하여 필터링 조건 재적용
- 각 RFM 지표 독립 검증
- `GROUP BY`를 사용한 집계 로직 적용
- 최종 고객 단위 데이터마트(`rfm`) 구축

일관된 비즈니스 로직 보장 및 분석 신뢰성 향상을 위한 단계입니다.

## 10. RFM 분석 (Python & SQL)

Python과 MySQL 양쪽에서 고객 단위 RFM 지표를 계산했습니다.

- **Recency**: 고객의 가장 최근 구매 이후 경과 일수
- **Frequency**: 고객별 주문 수
- **Monetary**: 고객별 총 구매 금액

### Python 기반 분석
- Jupyter Notebook에서 Pandas로 탐색적 분석 수행
- 유연한 분석을 위한 스코어링 및 세그멘테이션 로직 적용

### SQL 기반 분석

MySQL에서 두 단계로 RFM 지표를 계산했습니다:

1. **지표 단위 검증**
   - `sql/01_calculate_monetary.sql`: 고객별 총 구매액 검증
   - `sql/02_calculate_frequency.sql`: 고객별 주문 수 검증
   - `sql/03_calculate_recency.sql`: 최근 트랜잭션 기반 Recency 검증

2. **데이터마트 구축**
   - `sql/04_create_rfm_table.sql`: 모든 지표를 통합하여 최종 `rfm` 테이블 생성

최종 데이터셋 구축 전 각 지표를 독립적으로 검증하는 방식입니다.

## 11. 분석 & 시각화

### Python

Python으로 탐색적 분석과 고객 세그멘테이션 결과의 사전 검증을 수행했습니다.

- 세그먼트 분포 시각화
- RFM 기반 세그먼트 분포 분석
- 대시보드 개발 전 세그멘테이션 로직 기준 검증

![세그먼트 분포](images/segment_distribution.png)

### Tableau

고객 세그멘테이션과 매출 기여도를 종합적으로 보여주는 인터랙티브 Tableau 대시보드를 개발했습니다.

대시보드 포함 내용:

- 고객 세그먼트 분포
- RFM 산점도 분석
- 세그먼트별 매출 기여도

필터를 통해 고객 행동 탐색, 고가치 세그먼트 식별, 매출 집중도 분석이 가능합니다.

![RFM 대시보드](images/dashboard.png)

## 12. 결과 & 인사이트

주요 분석 결과:

- 대다수 고객은 **일반(Normal)** 세그먼트에 속하며 평균적인 구매 행동을 보임
- 소수의 **VIP** 고객이 총 매출의 불균형적으로 높은 비중을 차지
- **최근 구매 고객(Recent)**은 리텐션 및 타겟 참여에 높은 잠재력 보유
- **고액 지출 고객(Big Spenders)**은 상대적으로 낮은 구매 빈도에도 높은 매출 창출
- 매출이 **영국**에 고도로 집중되어 있어 지역 의존도 리스크 존재

소수의 고객이 매출의 상당 부분을 차지하는 강한 고객 가치 불균형이 확인됩니다.

RFM 기반 세그멘테이션은 고가치 고객 식별과 타겟 프로모션, 리텐션 캠페인, 고객 우선순위 설정 등 데이터 기반 마케팅 전략 수립을 가능하게 합니다.

### 비즈니스 시사점

- **VIP 고객**은 로열티 프로그램 및 신제품 얼리 액세스 우선 대상 — VIP 1명 이탈의 매출 영향이 큼
- **최근 구매 고객**은 참여도가 높을 때 업셀 캠페인의 최적 타겟
- **구매 빈도가 낮은 고액 지출 고객**은 묶음 상품이나 구독 모델로 구매 주기를 높일 수 있음
- **영국 시장 집중**은 지역 확장 기회이자, 영국 수요 약화 시 리스크 요인

## 13. 핵심 수치

- MySQL에 **397,884건** 트랜잭션 처리 및 적재
- **4,338명** 고객 분석
- 전체 고객의 **8.02%**만이 VIP 세그먼트
- VIP 고객이 총 매출의 **43.82%** 기여
- 고객 구매 행동에서 강한 파레토 분포 확인

## 14. 프로젝트 구조

```bash
online-retail-analysis/
├── data/                 # 원시 데이터셋 및 RFM 내보내기 데이터
│   ├── online_retail.csv
│   └── rfm_tableau.csv
├── images/               # 시각화 결과물 (Python 분석 & Tableau 대시보드)
│   ├── segment_distribution.png
│   ├── dashboard.png
│   └── data_model_erd.png
├── notebooks/            # 탐색적 분석 및 RFM 세그멘테이션
│   └── rfm_analysis.ipynb
├── scripts/              # Python 기반 데이터 정제 및 적재 파이프라인
│   └── preprocess_and_load.py
├── sql/                  # 지표 검증 및 RFM 데이터마트 구축 SQL 쿼리
│   ├── 00_create_online_retail.sql
│   ├── 01_calculate_monetary.sql
│   ├── 02_calculate_frequency.sql
│   ├── 03_calculate_recency.sql
│   └── 04_create_rfm_table.sql
├── tableau/              # Tableau 대시보드
│   └── rfm_dashboard.twbx
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── README.ko.md
```

## 15. 실행 방법

### 1) 저장소 클론

```bash
git clone https://github.com/hyunsung6608/online-retail-rfm-analysis.git
cd online-retail-rfm-analysis
```

### 2) 의존성 설치

```bash
pip install -r requirements.txt
```

> **요구사항:** SQL 스크립트에서 CTE를 사용하므로 **MySQL 8.0 이상**이 필요합니다.

### 3) MySQL 데이터베이스 준비

`retail_project` 데이터베이스 생성:

```bash
mysql -u your_username -p
```

```sql
CREATE DATABASE retail_project;
```

### 4) 환경 변수 설정

`.env.example`을 기반으로 `.env` 파일 생성:

```bash
# macOS / Linux
cp .env.example .env

# Windows
copy .env.example .env
```

`.env` 파일 수정:

```env
DB_USER = your_username
DB_PASSWORD = your_password
DB_HOST = localhost
DB_PORT = 3306
DB_NAME = retail_project
```

### 5) 테이블 스키마 생성

```bash
mysql -u your_username -p retail_project < sql/00_create_online_retail.sql
```

### 6) 데이터 전처리 파이프라인 실행

```bash
python scripts/preprocess_and_load.py
```

* Python으로 원시 데이터 정제
* 정제된 데이터를 MySQL에 적재

### 7) SQL 파이프라인 실행

아래 순서로 SQL 파일 실행:

```text
01_calculate_monetary.sql
02_calculate_frequency.sql
03_calculate_recency.sql
04_create_rfm_table.sql
```

* 1~3단계: 각 RFM 지표 검증
* 4단계: 최종 고객 단위 데이터마트(`rfm`) 구축

### 8) 분석 노트북 실행

```bash
cd notebooks
jupyter notebook
```

`rfm_analysis.ipynb`를 열어 결과 및 세그멘테이션을 확인합니다.

## 16. 향후 개선 사항

- Champions, At Risk, Hibernating 등 세분화된 RFM 세그멘테이션 규칙 적용으로 고객 분류 정확도 향상
- Python 기반 및 SQL 기반 RFM 계산 간 일관성 강화로 데이터 검증 신뢰성 향상
- 고객 세그멘테이션 주기적 업데이트를 위한 자동화 파이프라인 구축
- Customer Lifetime Value(CLV) 및 이탈 예측 등 추가 피처로 분석 모델 확장
- 상품 또는 시간 차원 추가를 통한 데이터 모델링 고도화
