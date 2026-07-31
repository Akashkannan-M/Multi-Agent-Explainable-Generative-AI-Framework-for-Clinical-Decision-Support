import sqlite3
from datetime import datetime

# Connect to database
connection = sqlite3.connect("database/clinical.db")

cursor = connection.cursor()

# Sample Patient Data
name = "Akash"
age = 21
gender = "Male"
disease = "Common Cold"

prediction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Insert Data
cursor.execute("""
INSERT INTO patients
(name, age, gender, disease, prediction_date)

VALUES (?, ?, ?, ?, ?)
""", (name, age, gender, disease, prediction_date))

connection.commit()

connection.close()

print("Patient Saved Successfully")