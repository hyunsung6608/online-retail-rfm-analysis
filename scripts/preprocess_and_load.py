import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from pathlib import Path

# 현재 파일 기준으로 프로젝트 루트 경로 계산
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
DATA_PATH = BASE_DIR / "data" / "online_retail.csv"

# .env 로드
load_dotenv(dotenv_path = ENV_PATH)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "retail_project")

if not DB_USER or not DB_PASSWORD:
    raise ValueError("DB_USER and DB_PASSWORD must be set in the .env file.")

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

df = pd.read_csv(DATA_PATH)

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

df = df.dropna(subset=["CustomerID"])
df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

df["CustomerID"] = df["CustomerID"].astype(int)

df["Sales"] = df["Quantity"] * df["UnitPrice"]

with engine.begin() as conn:
    conn.execute(text("TRUNCATE TABLE online_retail"))

df.to_sql(name="online_retail", con=engine, if_exists="append", index=False)

print("Data preprocessing and loading completed successfully.")
print(f"Loaded rows: {len(df)}")
print(f"Loaded file: {DATA_PATH}")