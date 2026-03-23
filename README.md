# Online Retail RFM Analysis

## 1. Project Overview
This project analyzes customer purchasing behavior using RFM (Recency, Frequency, Monetary) analysis based on the Online Retail dataset.
A data pipeline was built to preprocess raw data using Python and load it into MySQL, followed by SQL-based analysis to compute customer-level RFM metrics.
The goal of this project is to identify valuable customer segments and demonstrate an end-to-end data workflow from data preprocessing to analytical querying.

## 📊 Project Summary

- Built an end-to-end data pipeline using Python and MySQL  
- Performed RFM analysis using both Pandas and SQL  
- Identified high-value customer segments for business insights

## 2. Dataset
This project uses the Online Retail dataset, which contains transactional records of a UK-based online retail company.

Key columns include:
- `InvoiceNo`: Order identifier
- `StockCode`: Product code
- `Description`: Product name
- `Quantity`: Number of items purchased
- `InvoiceDate`: Transaction timestamp
- `UnitPrice`: Price per item
- `CustomerID`: Customer identifier
- `Country`: Customer country

This dataset is suitable for RFM analysis because it contains customer-level purchase history, order frequency, and monetary information.

## 3. Data Processing Pipeline
The project follows an end-to-end workflow:

1. Load raw transaction data from CSV
2. Clean and preprocess data using Python
3. Create a derived `Sales` column (`Quantity * UnitPrice`)
4. Load the cleaned dataset into MySQL
5. Calculate RFM metrics using SQL
6. Build a customer-level RFM table
7. Perform RFM analysis, customer segmentation, and exploratory analysis in Jupyter Notebook

## 4. Data Preprocessing (Python)

The raw dataset was cleaned in Python before loading it into MySQL.

Preprocessing steps:
- Converted `InvoiceDate` to datetime format
- Removed rows with missing `CustomerID`
- Excluded returned transactions (`Quantity <= 0`)
- Removed invalid price records (`UnitPrice <= 0`)
- Converted `CustomerID` to integer type
- Created a new `Sales` column as `Quantity * UnitPrice`

The preprocessing logic is implemented in:
- `scripts/preprocess_and_load.py`

After preprocessing, the cleaned data was loaded into MySQL for SQL-based analysis.

## 5. RFM Analysis (Python & SQL)

Customer-level RFM metrics were calculated using both Python and MySQL.

- **Recency**: Number of days since the customer's most recent purchase
- **Frequency**: Number of distinct orders made by each customer
- **Monetary**: Total purchase amount spent by each customer

### Python-based Analysis
RFM metrics were first computed using Pandas in Jupyter Notebook.  
Customer segmentation was performed by applying scoring and grouping logic, enabling flexible exploratory analysis.

### SQL-based Analysis
RFM metrics were also computed using SQL in MySQL to demonstrate database-level processing and reproducibility.  
The results were stored in an `rfm` table for further use.

SQL files used:
- `sql/01_calculate_monetary.sql`
- `sql/02_calculate_frequency.sql`
- `sql/03_calculate_recency.sql`
- `sql/04_create_rfm_table.sql`

## 6. Results & Insights

Key findings from the analysis include:

- The majority of customers fall into the **Normal** segment
- A smaller group of **VIP** customers contributes disproportionately high purchase value
- **Recent** customers show potential for retention campaigns
- **Big Spender** customers spend large amounts even if their purchase frequency is not the highest
- Sales are heavily concentrated in the **United Kingdom**

These results demonstrate how RFM analysis can be used to identify high-value customers and support targeted marketing strategies.

RFM scoring and segmentation were applied to classify customers into meaningful groups such as VIP, Normal, and Big Spender.

## 📊 Visualization

### Customer Segmentation Distribution
![Segment Distribution](images/segment_distribution.png)

## 7. Tech Stack

- **Python**
- **Pandas**
- **NumPy**
- **SQLAlchemy**
- **PyMySQL**
- **MySQL**
- **Jupyter Notebook**
- **Matplotlib**

## 8. Project Structure

```bash
online-retail-analysis/
├── data/
│   └── online_retail.csv
├── notebooks/
│   └── rfm_analysis.ipynb
├── scripts/
│   └── preprocess_and_load.py
├── sql/
│   ├── 01_calculate_monetary.sql
│   ├── 02_calculate_frequency.sql
│   ├── 03_calculate_recency.sql
│   └── 04_create_rfm_table.sql
├── requirements.txt
└── README.md
```

## 9. How to Run
### 1) Install dependencies
```bash
pip install -r requirements.txt
```
### 2) Prepare MySQL database

Create a database named retail_project in MySQL.

### 3) Update database connection

Edit the connection string in scripts/preprocess_and_load.py:

```python
engine = create_engine("mysql+pymysql://root:YOUR_PASSWORD@localhost/retail_project")
```
### 4) Run preprocessing script
```bash
python scripts/preprocess_and_load.py
```
### 5) Execute SQL files

Run the SQL files in the sql/ directory in order:

01_calculate_monetary.sql

02_calculate_frequency.sql

03_calculate_recency.sql

04_create_rfm_table.sql

### 6) Run Jupyter Notebook
jupyter notebook

## 10. Future Improvements

- Add customer segmentation rules directly in SQL

- Build a dashboard for RFM segment visualization

- Automate the pipeline with scheduled execution

- Extend analysis with cohort analysis or customer lifetime value (CLV)