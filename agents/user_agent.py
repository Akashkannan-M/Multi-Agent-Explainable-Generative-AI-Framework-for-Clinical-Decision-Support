import sqlite3
import pandas as pd


class UserAgent:

    def get_users(self):

        conn = sqlite3.connect("database/clinical.db")

        df = pd.read_sql_query(
            "SELECT user_id, username, role FROM users",
            conn
        )

        conn.close()

        return df

    def search_user(self, username):

        conn = sqlite3.connect("database/clinical.db")

        query = """
        SELECT user_id, username, role
        FROM users
        WHERE username LIKE ?
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=(f"%{username}%",)
        )

        conn.close()

        return df

    def add_user(self, username, password, role):
        
        conn = sqlite3.connect("database/clinical.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users(username, password, role)
            VALUES(?,?,?)
            """,
            (username, password, role)
        )

        conn.commit()
        conn.close()

    def delete_user(self, user_id):

        conn = sqlite3.connect("database/clinical.db")
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM users WHERE id=?",
            (user_id,)
        )

        conn.commit()
        conn.close()

    def total_users(self):

        conn = sqlite3.connect("database/clinical.db")
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM users")

        total = cursor.fetchone()[0]

        conn.close()

        return total