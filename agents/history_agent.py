import sqlite3
import pandas as pd


class HistoryAgent:

    # Get all patients
    def get_patients(self):

        conn = sqlite3.connect("database/clinical.db")

        query = "SELECT * FROM patients"

        df = pd.read_sql_query(query, conn)

        conn.close()

        return df


    # Get patient's own history
    def patient_history(self, username):

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
            params=(username,)
        )

        conn.close()

        return df


    # Search patient
    def search_patient(self, keyword):

        conn = sqlite3.connect("database/clinical.db")

        query = """
        SELECT *
        FROM patients
        WHERE name LIKE ?
        OR disease LIKE ?
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=(f"%{keyword}%", f"%{keyword}%")
        )

        conn.close()

        return df


    # Export to Excel
    def export_excel(self):

        df = self.get_patients()

        file_name = "Patient_History.xlsx"

        df.to_excel(file_name, index=False)

        return file_name
    
    def delete_patient(self, patient_id):
        conn = sqlite3.connect("database/clinical.db")
        
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM patients WHERE patient_id=?",
            (patient_id,)
        )
        
        conn.commit()
        
        conn.close()
        
    def update_patient(self, patient_id, name, age, gender, disease):
        
        conn = sqlite3.connect("database/clinical.db")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE patients
            SET
                name=?,
                age=?,
                gender=?,
                disease=?
                WHERE patient_id=?
        
        """, (name, age, gender, disease, patient_id))
        conn.commit()
        conn.close()