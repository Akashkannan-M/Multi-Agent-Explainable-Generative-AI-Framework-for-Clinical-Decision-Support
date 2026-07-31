import sqlite3
import pandas as pd

conn = sqlite3.connect("database/clinical.db")

df = pd.read_sql_query("SELECT * FROM patients", conn)

print(df)

conn.close()