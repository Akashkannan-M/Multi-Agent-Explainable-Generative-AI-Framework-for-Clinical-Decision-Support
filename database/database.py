import sqlite3
import os

DB_PATH = os.path.join("database", "clinical.db")


def _connect():
    # Ensure the database directory exists
    os.makedirs("database", exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_database():
    """Create all tables and default seed data if they do not exist.
    Idempotent - safe to call on every app startup.
    """
    conn = _connect()
    cursor = conn.cursor()

    # ------------------------------------------------------------
    # Patients
    # ------------------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients(
        patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT,
        disease TEXT,
        prediction_date TEXT,
        doctor_name TEXT,
        treatment TEXT
    )
    """)

    # Add treatment column if missing (older DBs)
    try:
        cursor.execute("ALTER TABLE patients ADD COLUMN treatment TEXT")
    except Exception:
        pass

    # ------------------------------------------------------------
    # Users
    # ------------------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # ------------------------------------------------------------
    # Chat History
    # ------------------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT,
        chat_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ------------------------------------------------------------
    # Appointments
    # ------------------------------------------------------------
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

    # ------------------------------------------------------------
    # Prescriptions
    # ------------------------------------------------------------
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

    # ------------------------------------------------------------
    # Medicines
    # ------------------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicines(
        medicine_id INTEGER PRIMARY KEY AUTOINCREMENT,
        medicine_name TEXT,
        quantity INTEGER,
        expiry_date TEXT,
        manufacturer TEXT
    )
    """)

    # ------------------------------------------------------------
    # Doctors
    # ------------------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors(
        doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_name TEXT,
        specialization TEXT,
        experience TEXT,
        phone TEXT
    )
    """)

    # ------------------------------------------------------------
    # Billing (used by Analytics & Admin Dashboard)
    # ------------------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS billing(
        bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        consultation_fee REAL,
        medicine_charge REAL,
        lab_charge REAL,
        total_amount REAL,
        bill_date TEXT
    )
    """)

    conn.commit()

    # ------------------------------------------------------------
    # Seed default users (admin, doctor)
    # ------------------------------------------------------------
    default_users = [
        ("admin", "admin123", "Admin"),
        ("doctor", "doctor123", "Doctor"),
        ("patient", "patient123", "Patient"),
    ]
    for u in default_users:
        try:
            cursor.execute(
                "INSERT INTO users(username, password, role) VALUES(?,?,?)",
                u,
            )
        except Exception:
            pass

    # ------------------------------------------------------------
    # Prevent duplicate doctors going forward.
    # 1. Deduplicate any rows that already exist in the doctors table.
    # 2. Add a UNIQUE index so future inserts cannot create duplicates.
    # 3. Seed default doctors only if they are NOT already present.
    # ------------------------------------------------------------
    cursor.execute("""
        DELETE FROM doctors
        WHERE doctor_id NOT IN (
            SELECT MIN(doctor_id)
            FROM doctors
            GROUP BY doctor_name, specialization
        )
    """)
    cursor.execute("DELETE FROM doctors WHERE doctor_name IS NULL OR doctor_name = ''")
    cursor.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS idx_doctors_name_spec "
        "ON doctors(doctor_name, specialization)"
    )

    default_doctors = [
        ("Dr. John", "General Physician", "10", "9876543210"),
        ("Dr. Kumar", "Cardiologist", "12", "9876543211"),
        ("Dr. Priya", "Dermatologist", "8", "9876543212"),
    ]
    for doc in default_doctors:
        cursor.execute(
            "SELECT COUNT(*) FROM doctors WHERE doctor_name=? AND specialization=?",
            (doc[0], doc[1]),
        )
        exists = cursor.fetchone()[0]
        if exists == 0:
            try:
                cursor.execute(
                    "INSERT INTO doctors(doctor_name, specialization, experience, phone) "
                    "VALUES(?,?,?,?)",
                    doc,
                )
            except Exception:
                pass

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_database()
    print("Database initialized successfully.")
