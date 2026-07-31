import sqlite3

conn = sqlite3.connect("database/clinical.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

users = [
    ("admin", "admin123", "Admin"),
    ("doctor", "doctor123", "Doctor"),
    ("staff", "staff123", "Staff")
]

for user in users:
    try:
        cursor.execute(
            "INSERT INTO users(username,password,role) VALUES(?,?,?)",
            user
        )
    except:
        pass

conn.commit()
conn.close()

print("Users table created successfully.")