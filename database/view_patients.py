import sqlite3

# Connect to Database
connection = sqlite3.connect("database/clinical.db")

cursor = connection.cursor()

# Read all patient records
cursor.execute("SELECT * FROM patients")

patients = cursor.fetchall()

print("\n----- Patient Records -----\n")

for patient in patients:
    print(patient)

connection.close()