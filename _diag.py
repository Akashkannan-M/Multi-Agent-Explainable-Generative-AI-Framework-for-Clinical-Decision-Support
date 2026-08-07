import sqlite3, os, json

print("CWD:", os.getcwd())
print("clinical.db exists:", os.path.exists("database/clinical.db"))
print("patient.db exists:", os.path.exists("database/patient.db"))
print("model exists:", os.path.exists("models/disease_model.pkl"))

conn = sqlite3.connect("database/clinical.db")
tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print("tables:", tables)

for t in ["users", "patients", "chat_history", "appointments", "prescriptions", "medicines", "doctors", "billing"]:
    if t in tables:
        cols = [x[1] for x in conn.execute(f"PRAGMA table_info({t})").fetchall()]
        print(f"[{t}] cols:", cols)
        try:
            rows = conn.execute(f"SELECT * FROM {t} LIMIT 3").fetchall()
            print(f"[{t}] sample rows:", rows)
        except Exception as e:
            print(f"[{t}] error:", e)
    else:
        print(f"[{t}] MISSING")

# check users
if "users" in tables:
    print("ALL USERS:", conn.execute("SELECT * FROM users").fetchall())

# check billing
if "billing" in tables:
    bcols = [x[1] for x in conn.execute("PRAGMA table_info(billing)").fetchall()]
    print("billing cols:", bcols)
else:
    print("billing table MISSING - monthly_revenue & admin revenue will fail")

conn.close()
