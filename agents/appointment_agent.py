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

    def get_appointments(self):

        conn = sqlite3.connect("database/clinical.db")

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