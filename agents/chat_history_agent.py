import sqlite3
import pandas as pd


class ChatHistoryAgent:

    def save_chat(self, question, answer):

        conn = sqlite3.connect("database/clinical.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO chat_history(question, answer)
            VALUES(?, ?)
            """,
            (question, answer)
        )

        conn.commit()
        conn.close()

    def get_history(self):

        conn = sqlite3.connect("database/clinical.db")

        df = pd.read_sql_query(
            """
            SELECT chat_id,
                   question,
                   answer,
                   chat_time
            FROM chat_history
            ORDER BY chat_time DESC
            """,
            conn
        )

        conn.close()

        return df