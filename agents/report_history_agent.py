import sqlite3
import pandas as pd


class ReportHistoryAgent:

    def get_reports(self):

        conn = sqlite3.connect("database/clinical.db")

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
        BETWEEN DATE(?) AND DATE(?)
        ORDER BY prediction_date DESC
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=(start_date, end_date)
        )

        conn.close()

        return df