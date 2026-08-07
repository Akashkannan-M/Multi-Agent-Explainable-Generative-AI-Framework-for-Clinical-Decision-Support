import sqlite3
import pandas as pd

class ReportHistoryAgent:

    def get_reports(self, username=None):

        conn = sqlite3.connect("database/clinical.db")

        if username:
            df = pd.read_sql_query(
                """
                SELECT *
                FROM patients
                WHERE name = ?
                ORDER BY prediction_date DESC
                """,
                conn,
                params=(username,)
            )
        else:
            df = pd.read_sql_query(
                "SELECT * FROM patients",
                conn
            )

        conn.close()

        return df

    def filter_reports(self, start_date, end_date):

        conn = sqlite3.connect("database/clinical.db")

        query = """
        SELECT *
        FROM patients
        WHERE DATE(prediction_date)
        BETWEEN ? AND ?
        ORDER BY prediction_date DESC
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=(start_date, end_date)
        )

        conn.close()

        return df

    def patient_reports(self, patient_name):

        conn = sqlite3.connect("database/clinical.db")

        query = """
        SELECT *
        FROM patients
        WHERE name = ?
        ORDER BY prediction_date DESC
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=(patient_name,)
        )

        conn.close()

        return df

    def patient_report_count(self, patient_name):

        conn = sqlite3.connect("database/clinical.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM patients
            WHERE name = ?
            """,
            (patient_name,)
        )

        count = cursor.fetchone()[0]

        conn.close()

        return count

    def patient_history(self, patient_name):

        conn = sqlite3.connect("database/clinical.db")

        query = """
        SELECT *
        FROM patients
        WHERE name = ?
        ORDER BY prediction_date DESC
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=(patient_name,)
        )

        conn.close()

        return df
