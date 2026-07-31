import sqlite3
from datetime import datetime

class PatientAgent:

    def save_patient(
        self,
        name,
        age,
        gender,
        disease,
        doctor_name,
        treatment
    ):

        connection = sqlite3.connect("database/clinical.db")
        cursor = connection.cursor()

        prediction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO patients
            (
                name,
                age,
                gender,
                disease,
                doctor_name,
                treatment,
                prediction_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            age,
            gender,
            disease,
            doctor_name,
            treatment,
            prediction_date
        ))

        connection.commit()
        connection.close()