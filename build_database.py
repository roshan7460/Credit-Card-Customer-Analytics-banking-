import sqlite3
from pathlib import Path
from data_generator import ensure_csvs

BASE = Path(__file__).resolve().parent
DB_PATH = BASE / "credit_card_analytics.db"
customers, transactions = ensure_csvs(BASE)
con = sqlite3.connect(DB_PATH)
with open(BASE / "schema.sql", "r", encoding="utf-8") as f:
    con.executescript(f.read())
customers.to_sql("customers", con, if_exists="append", index=False)
transactions.to_sql("transactions", con, if_exists="append", index=False)
con.commit()
con.close()
print(f"Database created: {DB_PATH}")
