import sqlite3
import pandas as pd


class DoctorAnalyticsAgent:

    def doctor_patient_count(self):

        conn = sqlite3.connect("database/clinical.db")

        df = pd.read_sql_query("""
            SELECT
                doctor_name,
                COUNT(*) AS total_patients
            FROM patients
            GROUP BY doctor_name
            ORDER BY total_patients DESC
        """, conn)

        conn.close()

        return df


    def doctor_specialization(self):

        conn = sqlite3.connect("database/clinical.db")

        df = pd.read_sql_query("""
            SELECT
                doctor_name,
                specialization
            FROM doctors
        """, conn)

        conn.close()

        return df


    def patient_treatment_history(self):

        conn = sqlite3.connect("database/clinical.db")

        df = pd.read_sql_query("""
            SELECT
                name AS patient_name,
                doctor_name,
                disease,
                treatment
            FROM patients
            ORDER BY patient_id DESC
        """, conn)

        conn.close()

        return df