import sqlite3
import pandas as pd


class MedicineAgent:

    def add_medicine(
        self,
        medicine_name,
        quantity,
        expiry_date,
        manufacturer
    ):

        conn = sqlite3.connect("database/clinical.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO medicines
            (
                medicine_name,
                quantity,
                expiry_date,
                manufacturer
            )
            VALUES(?,?,?,?)
            """,
            (
                medicine_name,
                quantity,
                expiry_date,
                manufacturer
            )
        )

        conn.commit()
        conn.close()


    def get_medicines(self):

        conn = sqlite3.connect("database/clinical.db")

        df = pd.read_sql_query(
            """
            SELECT *
            FROM medicines
            ORDER BY expiry_date
            """,
            conn
        )

        conn.close()

        return df
    
    def low_stock(self):
        conn = sqlite3.connect("database/clinical.db")
        df = pd.read_sql_query(
            """
            SELECT *
            FROM medicines
            WHERE quantity <= 10
            """,
            conn
        )

        conn.close()

        return df


    def expired_medicines(self):

        conn = sqlite3.connect("database/clinical.db")

        df = pd.read_sql_query(
            """
            SELECT *
            FROM medicines
            WHERE DATE(expiry_date) < DATE('now')
            ORDER BY expiry_date
            """,
            conn
        )

        conn.close()

        return df