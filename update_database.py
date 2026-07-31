import sqlite3

conn = sqlite3.connect("database/clinical.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE patients ADD COLUMN doctor_name TEXT")
    print("doctor_name column added successfully.")
except Exception as e:
    print(e)

conn.commit()
conn.close()