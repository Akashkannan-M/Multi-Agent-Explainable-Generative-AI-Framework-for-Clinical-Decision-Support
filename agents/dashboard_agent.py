import sqlite3


class DashboardAgent:

    def get_dashboard(self):

        conn = sqlite3.connect("database/clinical.db")
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM patients")
        total_patients = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT disease) FROM patients")
        total_diseases = cursor.fetchone()[0]

        cursor.execute("""
            SELECT disease, COUNT(*)
            FROM patients
            GROUP BY disease
            ORDER BY COUNT(*) DESC
            LIMIT 1
        """)
        result = cursor.fetchone()

        if result:
            common_disease = result[0]
        else:
            common_disease = "None"

        cursor.execute("SELECT COUNT(*) FROM patients WHERE gender='Male'")
        male = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM patients WHERE gender='Female'")
        female = cursor.fetchone()[0]

        conn.close()

        return {
            "patients": total_patients,
            "diseases": total_diseases,
            "common": common_disease,
            "male": male,
            "female": female
        }
    
    def disease_count(self):
        import sqlite3
        import pandas as pd
        
        conn = sqlite3.connect("database/clinical.db")
        
        query = """
        SELECT disease, COUNT(*) AS count
        FROM patients
        GROUP BY disease
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def disease_bar_chart(self):
        import sqlite3
        import pandas as pd
        
        conn = sqlite3.connect("database/clinical.db")
        query = """
        SELECT disease,
           COUNT(*) AS count
        FROM patients
        GROUP BY disease
        """
        df = pd.read_sql_query(query, conn)
        
        conn.close()
        
        return df
    
    def disease_statistics(self):
        import sqlite3
        import pandas as pd
        conn = sqlite3.connect("database/clinical.db")
        query = """
        SELECT
            disease,
            COUNT(*) AS Patients
        FROM patients
        GROUP BY disease
        ORDER BY Patients DESC
        """
        
        df = pd.read_sql_query(query, conn)
        
        conn.close()
        
        return df
    
    def gender_statistics(self):
        import sqlite3
        import pandas as pd
        conn = sqlite3.connect("database/clinical.db")
        
        query = """
        SELECT
            gender,
            COUNT(*) AS count
        FROM patients
        GROUP BY gender
        """
        df = pd.read_sql_query(query, conn)
        
        conn.close()
        
        return df
    
    def prediction_timeline(self):
        import sqlite3
        import pandas as pd

        conn = sqlite3.connect("database/clinical.db")

        query = """
        SELECT
            DATE(prediction_date) AS date,
            COUNT(*) AS count
        FROM patients
        GROUP BY DATE(prediction_date)
        ORDER BY DATE(prediction_date)
        """

        df = pd.read_sql_query(query, conn)

        conn.close()

        return df

    def top5_diseases(self):

        import sqlite3
        import pandas as pd

        conn = sqlite3.connect("database/clinical.db")

        query = """
        SELECT
            disease,
            COUNT(*) AS count
        FROM patients
        GROUP BY disease
        ORDER BY count DESC
        LIMIT 5
        """

        df = pd.read_sql_query(query, conn)

        conn.close()

        return df

    def daily_prediction(self):

        import sqlite3
        import pandas as pd

        conn = sqlite3.connect("database/clinical.db")

        query = """
        SELECT
            DATE(prediction_date) AS Date,
            COUNT(*) AS Patients
        FROM patients
        GROUP BY DATE(prediction_date)
        ORDER BY DATE(prediction_date)
        """

        df = pd.read_sql_query(query, conn)

        conn.close()

        return df
    
    def filter_by_date(self, start_date, end_date):
        import sqlite3
        import pandas as pd

        conn = sqlite3.connect("database/clinical.db")

        query = """
        SELECT *
        FROM patients
        WHERE DATE(prediction_date)
        BETWEEN ? AND ?
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=(start_date, end_date)
        )

        conn.close()

        return df
    
    
        