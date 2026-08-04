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

    def get_prescriptions(self, username=None):

        conn = sqlite3.connect("database/clinical.db")

        if username:
            df = pd.read_sql_query(
                """
                SELECT *
                FROM prescriptions
                WHERE patient_name = ?
                ORDER BY prescription_date DESC
                """,
                conn,
                params=(username,)
            )
        else:
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
    
    def patient_prescription_count(self, username):

        import sqlite3

        conn = sqlite3.connect(
            "database/clinical.db"
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM prescriptions
            WHERE patient_name=?
            """,
            (username,)
        )

        count = cursor.fetchone()[0]

        conn.close()

        return count
    
    
    def patient_prescriptions(self, patient_name):

        conn = sqlite3.connect("database/clinical.db")

        query = """
        SELECT *
        FROM prescriptions
        WHERE patient_name = ?
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=(patient_name,)
        )

        conn.close()

        return df