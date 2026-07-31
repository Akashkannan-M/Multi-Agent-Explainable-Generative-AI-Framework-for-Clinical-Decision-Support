import sqlite3
import pandas as pd


class AnalyticsAgent:

    def total_patients(self):

        conn = sqlite3.connect("database/clinical.db")
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM patients")

        total = cursor.fetchone()[0]

        conn.close()

        return total


    def today_patients(self):

        conn = sqlite3.connect("database/clinical.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT COUNT(*)
        FROM patients
        WHERE DATE(prediction_date)=DATE('now')
        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total


    def monthly_revenue(self):

        conn = sqlite3.connect("database/clinical.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT IFNULL(SUM(total_amount),0)
        FROM billing
        WHERE strftime('%Y-%m',bill_date)=strftime('%Y-%m','now')
        """)

        revenue = cursor.fetchone()[0]

        conn.close()

        return revenue


    def disease_statistics(self):

        conn = sqlite3.connect("database/clinical.db")

        df = pd.read_sql_query("""
        SELECT disease,
               COUNT(*) AS Total
        FROM patients
        GROUP BY disease
        """, conn)

        conn.close()

        return df


    def appointment_statistics(self):

        conn = sqlite3.connect("database/clinical.db")

        df = pd.read_sql_query("""
        SELECT status,
               COUNT(*) AS Total
        FROM appointments
        GROUP BY status
        """, conn)

        conn.close()

        return df