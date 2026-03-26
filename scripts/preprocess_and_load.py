import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# .env 로드
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "retail_project")

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

DATA_PATH = "../data/online_retail.csv"
df = pd.read_csv(DATA_PATH)

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

df = df.dropna(subset=["CustomerID"])
df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

df["CustomerID"] = df["CustomerID"].astype(int)

df["Sales"] = df["Quantity"] * df["UnitPrice"]

df.to_sql(name="online_retail", con=engine, if_exists="replace", index=False)

print("Data preprocessing and loading completed successfully.")
print(f"Loaded rows: {len(df)}")