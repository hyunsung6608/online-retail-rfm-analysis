# Online Retail RFM Analysis

## 1. Project Overview

Customer value is not evenly distributed.
A small group of high-value customers often drives
the majority of revenue — yet without proper segmentation,
they are treated the same as average buyers.

This project applies RFM (Recency, Frequency, Monetary)
analysis to identify and segment customers based on
purchasing behavior, using an end-to-end pipeline
from raw transaction data to an interactive Tableau dashboard.

Key highlight: The Champions segment (R≥4, F≥4, M≥4) comprises **22.18%** of customers
yet contributes **65.19%** of total revenue —
confirming a strong Pareto-like distribution in customer value.

## 2. Key Highlights

- Processed **397,884** transactions and analyzed **4,338** unique customers
- Champions segment (**22.18%** of customers) contributes **65.19%** of total revenue — confirming a strong Pareto-like distribution
- Segmented customers into **9 distinct groups** for precise, actionable targeting
- Built end-to-end pipeline: Python cleaning → MySQL data mart → Tableau dashboard
- Each RFM metric independently validated in SQL before data mart construction
- Applied **log transformation to Monetary** (`log1p`) to reduce outlier distortion in M_score

## 3. Project Flow

Raw CSV → Python Data Cleaning & Exploratory Analysis → MySQL Loading → SQL-based Transformation & Validation → RFM Data Mart Construction → Python/Tableau Visualization

## 4. Data Model & Data Mart Design

![Data Model ERD](images/data_model_erd.png)

This project is designed with a clear separation between transactional data and an analysis-ready customer-level data mart.

Transaction-level data (`online_retail`) is transformed and aggregated into customer-level metrics (R/F/M), which are stored in the `rfm` table.

This structure enables efficient customer segmentation and supports scalable, reproducible analytics workflows.

### Data Model Overview

The data model consists of two main layers:

- **Transaction-level table (`online_retail`)**
  - Stores cleaned transactional data loaded into MySQL
  - Contains detailed information such as `InvoiceNo`, `StockCode`, `Quantity`, `UnitPrice`, `CustomerID`, and `InvoiceDate`

- **Customer-level data mart (`rfm`)**
  - Aggregated table derived from transaction data
  - One row per customer
  - Stores RFM metrics (`Recency`, `Frequency`, `Monetary`) for segmentation and analysis

### Data Mart Design

A customer-centric data mart was designed to support behavioral analysis.

- The `rfm` table serves as a **subject-oriented analytical table**
- Transaction-level data is transformed into customer-level metrics through SQL-based aggregation
- The structure is optimized for analytical queries, visualization, and business insights

### Data Transformation Logic

The transformation from raw data to the data mart includes:

- Data validation:
  - Missing `CustomerID` removed
  - Returned transactions excluded (`Quantity <= 0`)
  - Invalid price records filtered (`UnitPrice <= 0`)
- Feature engineering:
  - `Sales = Quantity × UnitPrice`
- Aggregation:
  - **Recency**: Days since last purchase
  - **Frequency**: Number of distinct orders per customer
  - **Monetary**: Total spending per customer

### Design Rationale

- Raw data is preserved at the transaction level for traceability
- Aggregated data is separated into a dedicated analytical table for performance and clarity
- SQL-based transformation ensures reproducibility and consistency in analytical results
- The data mart structure supports scalable customer segmentation and downstream analytics

## 5. Project Summary

- Built an end-to-end data pipeline combining Python and MySQL
- Performed data cleaning in Python and SQL-based validation and aggregation
- Designed and constructed a customer-level RFM data mart
- Applied RFM analysis to segment customers into 9 groups based on purchasing behavior
- Identified high-value customer groups and generated actionable business insights

## 6. Tech Stack

- **Language**: Python, SQL
- **Data Processing**: Pandas, NumPy
- **Database**: MySQL
- **ORM / Connection**: SQLAlchemy, PyMySQL
- **Visualization**: Matplotlib, Tableau
- **Environment Management**: python-dotenv
- **Notebook**: Jupyter Notebook
- **Development Environment**: VS Code
- **Concepts**: Data Cleaning, Data Transformation, Data Validation, Data Mart Design

## 7. Dataset

This project uses the Online Retail dataset, which contains transactional records of a UK-based online retail company.

The dataset captures detailed purchase history at the transaction level, making it suitable for customer behavior analysis and RFM-based segmentation.

Key columns include:
- `InvoiceNo`: Order identifier
- `StockCode`: Product code
- `Description`: Product name
- `Quantity`: Number of items purchased
- `InvoiceDate`: Transaction timestamp
- `UnitPrice`: Price per item
- `CustomerID`: Customer identifier
- `Country`: Customer country

This dataset enables the calculation of customer-level metrics such as purchase recency, order frequency, and total spending, which are essential for building a customer-level analytical data mart.

## 8. Data Processing Pipeline

The project follows an end-to-end data pipeline from raw data ingestion to analytical data mart construction:

1. Load raw transaction data from CSV
2. Perform data cleaning and validation using Python
3. Create a derived `Sales` column (`Quantity * UnitPrice`)
4. Load the cleaned dataset into MySQL
5. Apply SQL-based transformation and metric validation
6. Aggregate transaction-level data into a customer-level RFM data mart (`rfm`)
7. Perform analysis, segmentation, and visualization in Python and Tableau

## 9. Data Preprocessing & Transformation

Data processing was performed in two stages using both Python and SQL to ensure data quality and analytical consistency.

### Python (Data Cleaning)

The raw dataset was cleaned before loading into MySQL.

- Converted `InvoiceDate` to datetime format
- Removed rows with missing `CustomerID`
- Excluded returned transactions (`Quantity <= 0`)
- Removed invalid price records (`UnitPrice <= 0`)
- Converted `CustomerID` to integer type
- Created a new `Sales` column as `Quantity * UnitPrice`

The preprocessing logic is implemented in `scripts/preprocess_and_load.py`.

### SQL (Data Validation & Aggregation)

SQL was used to validate metrics and construct the analytical dataset.

- Reapplied filtering conditions using a CTE (`clean_data`)
- Validated each RFM metric independently
- Applied aggregation logic using `GROUP BY`
- Constructed the final customer-level data mart (`rfm`)

These steps ensure consistent business logic and improve the reliability of the analysis.

## 10. RFM Analysis (Python & SQL)

Customer-level RFM metrics were calculated using both Python and MySQL.

- **Recency**: Days since the customer's most recent purchase
- **Frequency**: Number of distinct orders per customer
- **Monetary**: Total purchase amount per customer

### Python-based Analysis

- Performed exploratory analysis using Pandas in Jupyter Notebook
- Applied scoring and segmentation logic for flexible analysis
- **Applied log transformation (`log1p`) to Monetary before computing M_score** — prevents extreme outliers (e.g., a customer who spent £77,183 in a single order) from distorting the score distribution

### SQL-based Analysis

RFM metrics were calculated in MySQL using a two-step approach:

1. **Metric-level validation**
   - `sql/01_calculate_monetary.sql`: Validates total spending per customer
   - `sql/02_calculate_frequency.sql`: Validates order count per customer
   - `sql/03_calculate_recency.sql`: Validates recency based on latest transaction

2. **Data mart construction**
   - `sql/04_create_rfm_table.sql`: Integrates all metrics and creates the final `rfm` table

This approach ensures that each metric is independently verified before constructing the final analytical dataset.

## 11. Customer Segmentation

Customers are classified into 9 segments based on their R, F, and M scores (each scored 1–5).
Segmentation logic references score columns directly — not string indexing — for stability and clarity.

| Segment | R | F | M | Description |
|---|---|---|---|---|
| **Champions** | ≥ 4 | ≥ 4 | ≥ 4 | Best customers across all dimensions |
| **Can't Lose** | = 1 | ≥ 4 | ≥ 4 | Former top customers who have churned |
| **At Risk** | ≤ 2 | ≥ 3 | ≥ 3 | High-value customers showing churn signals |
| **Loyal** | ≥ 3 | ≥ 4 | ≥ 3 | Consistent, frequent, and valuable buyers |
| **Potential Loyalist** | ≥ 4 | ≥ 2 | ≥ 2 | Recent buyers with growth potential |
| **New Customer** | ≥ 4 | = 1 | — | First-time buyers with recent activity |
| **Need Attention** | = 3 | ≥ 2 | ≥ 2 | Mid-tier customers at risk of stagnation |
| **Hibernating** | ≤ 2 | ≤ 2 | — | Inactive customers with low activity |
| **Normal** | All others | | | General customers with average behavior |

## 12. Analysis & Visualization

### Python

Python was used for exploratory analysis and preliminary validation of customer segmentation results.

- Visualized the distribution of 9 customer segments
- Analyzed RFM-based segment proportions
- Validated segmentation logic before dashboard development

![Segment Distribution](images/segment_distribution.png)

### Tableau

An interactive Tableau dashboard was developed to provide a comprehensive view of customer segmentation and revenue contribution.

The dashboard includes:

- Customer Segment Distribution (9 segments, color-coded)
- RFM Scatter Analysis
- Revenue Contribution by Segment

Users can interact with filters to explore customer behavior, identify high-value segments, and analyze revenue concentration patterns.

![RFM Dashboard](images/dashboard.png)

## 13. Results & Insights

Key findings from the analysis include:

- **Champions** account for a small share of customers but drive a disproportionately large portion of revenue
- **Can't Lose** customers were once top buyers and require immediate Win-back campaigns
- **At Risk** customers are trending toward churn — retention action is urgent
- **Potential Loyalists** recently purchased and show strong upsell and membership conversion potential
- Sales are highly concentrated in the **United Kingdom**, suggesting geographic dependency risk

These results confirm a strong imbalance in customer value distribution, where a small segment drives a significant portion of total revenue.

### Business Implications

- **Champions** — Prioritize for loyalty programs and early access to new products
- **Can't Lose** — Offer premium incentives, launch immediate Win-back campaigns
- **At Risk** — Send personalized messages and re-engagement coupons
- **Loyal** — Drive upsell and cross-sell, nudge toward Champions tier
- **Potential Loyalist** — Encourage membership sign-up and repeat purchase rewards
- **New Customer** — Deploy onboarding emails and second-purchase coupons
- **Need Attention** — Target with seasonal promotions and purchase motivators
- **Hibernating** — Apply low-cost re-engagement or exclude from active campaigns
- **UK market concentration** — Represents both a geographic expansion opportunity and a concentration risk

## 14. Key Results

- Processed and loaded **397,884** transaction records into MySQL
- Analyzed **4,338** unique customers
- Segmented customers into **9 distinct groups** for targeted marketing
- Champions segment (**22.18%** of customers) contributes **65.19%** of total revenue
- Confirmed a strong Pareto-like distribution in customer purchasing behavior

## 15. Project Structure

```bash
online-retail-analysis/
├── data/                 # Raw dataset and exported RFM data
│   ├── online_retail.csv
│   └── rfm_tableau.csv
├── images/               # Visualization outputs (Python analysis & Tableau dashboard)
│   ├── segment_distribution.png
│   ├── dashboard.png
│   └── data_model_erd.png
├── notebooks/            # Exploratory analysis and RFM segmentation
│   └── rfm_analysis.ipynb
├── scripts/              # Python-based data cleaning and loading pipeline
│   └── preprocess_and_load.py
├── sql/                  # SQL queries for metric validation and RFM data mart construction
│   ├── 00_create_online_retail.sql
│   ├── 01_calculate_monetary.sql
│   ├── 02_calculate_frequency.sql
│   ├── 03_calculate_recency.sql
│   └── 04_create_rfm_table.sql
├── tableau/              # Tableau dashboard
│   └── rfm_dashboard.twbx
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── README.ko.md
```

## 16. How to Run

### 1) Clone the repository

```bash
git clone https://github.com/hyunsung6608/online-retail-rfm-analysis.git
cd online-retail-rfm-analysis
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

> **Requirement:** This project requires **MySQL 8.0+** because the SQL scripts use Common Table Expressions (CTEs).

### 3) Prepare MySQL database

Create a database named `retail_project`:

```bash
mysql -u your_username -p
```

```sql
CREATE DATABASE retail_project;
```

### 4) Set up environment variables

Create a `.env` file based on `.env.example`:

```bash
# macOS / Linux
cp .env.example .env

# Windows
copy .env.example .env
```

Edit the `.env` file:

```env
DB_USER = your_username
DB_PASSWORD = your_password
DB_HOST = localhost
DB_PORT = 3306
DB_NAME = retail_project
```

### 5) Create table schema

```bash
mysql -u your_username -p retail_project < sql/00_create_online_retail.sql
```

### 6) Run data preprocessing pipeline

```bash
python scripts/preprocess_and_load.py
```

* Cleans raw data using Python
* Loads processed data into MySQL

### 7) Execute SQL pipeline

Run the SQL files in order:

```text
01_calculate_monetary.sql
02_calculate_frequency.sql
03_calculate_recency.sql
04_create_rfm_table.sql
```

* Steps 1–3: Validate each RFM metric
* Step 4: Construct the final customer-level data mart (`rfm`)

### 8) Run analysis notebook

```bash
cd notebooks
jupyter notebook
```

Open `rfm_analysis.ipynb` to explore results and segmentation.

## 17. Future Improvements

- Ensure consistency between Python-based and SQL-based RFM calculations to strengthen data validation and reliability
- Build an automated data pipeline to enable periodic updates of customer segmentation and improve scalability
- Extend the analytical model by incorporating additional features such as Customer Lifetime Value (CLV) and churn prediction
- Improve data modeling by introducing additional dimensions (e.g., product or time) to support more advanced analysisd