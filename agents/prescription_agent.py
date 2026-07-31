import sqlite3
import pandas as pd


class PrescriptionAgent:

    def add_prescription(
        self,
        patient_name,
        doctor_name,
        diagnosis,
        medicines,
        dosage,
        advice,
        prescription_date
    ):

        conn = sqlite3.connect("database/clinical.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO prescriptions
            (
                patient_name,
                doctor_name,
                diagnosis,
                medicines,
                dosage,
                advice,
                prescription_date
            )
            VALUES(?,?,?,?,?,?,?)
            """,
            (
                patient_name,
                doctor_name,
                diagnosis,
                medicines,
                dosage,
                advice,
                prescription_date
            )
        )

        conn.commit()
        conn.close()

    def get_prescriptions(self):

        conn = sqlite3.connect("database/clinical.db")

        df = pd.read_sql_query(
            """
            SELECT *
            FROM prescriptions
            ORDER BY prescription_date DESC
            """,
            conn
        )

        conn.close()

        return df