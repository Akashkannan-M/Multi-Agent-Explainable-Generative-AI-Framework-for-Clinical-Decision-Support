import sqlite3
import pandas as pd


class AppointmentAgent:

    def book_appointment(
        self,
        patient_name,
        doctor_name,
        appointment_date,
        appointment_time
    ):

        conn = sqlite3.connect("database/clinical.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO appointments
            (
                patient_name,
                doctor_name,
                appointment_date,
                appointment_time,
                status
            )
            VALUES(?,?,?,?,?)
            """,
            (
                patient_name,
                doctor_name,
                appointment_date,
                appointment_time,
                "Pending"
            )
        )

        conn.commit()
        conn.close()

    def get_appointments(self, username=None):

        conn = sqlite3.connect("database/clinical.db")

        if username:
            df = pd.read_sql_query(
                """
                SELECT *
                FROM appointments
                WHERE patient_name = ?
                ORDER BY appointment_date DESC
                """,
                conn,
                params=(username,)
            )
        else:
            df = pd.read_sql_query(
                """
                SELECT *
                FROM appointments
                ORDER BY appointment_date DESC
                """,
                conn
            )

        conn.close()

        return df

    def update_status(self, appointment_id, status):

        conn = sqlite3.connect("database/clinical.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE appointments
            SET status=?
            WHERE appointment_id=?
            """,
            (
                status,
                appointment_id
            )
        )

        conn.commit()
        conn.close()
        
    def patient_appointment_count(self, username):

        import sqlite3

        conn = sqlite3.connect(
            "database/clinical.db"
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM appointments
            WHERE patient_name=?
            """,
            (username,)
        )

        count = cursor.fetchone()[0]

        conn.close()

        return count
    
    def patient_appointments(self, patient_name):

        conn = sqlite3.connect("database/clinical.db")

        query = """
        SELECT *
        FROM appointments
        WHERE patient_name = ?
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=(patient_name,)
        )

        conn.close()

        return df