import sqlite3

# Connect to Database
connection = sqlite3.connect("database/clinical.db")

# Create Cursor
cursor = connection.cursor()




print("doctor_name column checked.")

# Create Patient Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients(

    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    age INTEGER,

    gender TEXT,

    disease TEXT,

    prediction_date TEXT,
    
    doctor_name TEXT

)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history (
    chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    answer TEXT,
    chat_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments(

    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,

    patient_name TEXT,

    doctor_name TEXT,

    appointment_date TEXT,

    appointment_time TEXT,

    status TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS prescriptions(

    prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,

    patient_name TEXT,

    doctor_name TEXT,

    diagnosis TEXT,

    medicines TEXT,

    dosage TEXT,

    advice TEXT,

    prescription_date TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS medicines(

    medicine_id INTEGER PRIMARY KEY AUTOINCREMENT,

    medicine_name TEXT,

    quantity INTEGER,

    expiry_date TEXT,

    manufacturer TEXT
)
""")



cursor.execute("""
CREATE TABLE IF NOT EXISTS doctors(

    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,

    doctor_name TEXT,

    specialization TEXT
)
""")

try:
    cursor.execute("ALTER TABLE patients ADD COLUMN doctor_name TEXT")
except:
    pass

connection.commit()

connection.close()

print("Database Created Successfully")