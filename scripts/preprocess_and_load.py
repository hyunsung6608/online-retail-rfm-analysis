import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("../data/online_retail.csv")

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

df = df.dropna(subset=["CustomerID"])
df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

df["CustomerID"] = df["CustomerID"].astype(int)

df["Sales"] = df["Quantity"] * df["UnitPrice"]

engine = create_engine("mysql+pymysql://root:YOUR_PASSWORD@localhost/retail_project")  # 비밀번호 수정 필요

df.to_sql(name="online_retail", con=engine, if_exists="replace", index=False)

print("Data preprocessing and loading completed successfully.")
print(f"Loaded rows: {len(df)}")