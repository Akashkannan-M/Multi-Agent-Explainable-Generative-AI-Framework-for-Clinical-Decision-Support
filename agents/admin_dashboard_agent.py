import sqlite3


class AdminDashboardAgent:

    def get_dashboard(self):

        conn = sqlite3.connect("database/clinical.db")
        cursor = conn.cursor()

        # Total Users
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]

        # Total Patients
        cursor.execute("SELECT COUNT(*) FROM patients")
        total_patients = cursor.fetchone()[0]

        # Total Medicines
        cursor.execute("SELECT COUNT(*) FROM medicines")
        total_medicines = cursor.fetchone()[0]

        # Low Stock Medicines
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM medicines
            WHERE quantity <= 10
            """
        )
        low_stock = cursor.fetchone()[0]

        # Expired Medicines
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM medicines
            WHERE DATE(expiry_date) < DATE('now')
            """
        )
        expired = cursor.fetchone()[0]

        # Today's Appointments
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM appointments
            WHERE appointment_date = DATE('now')
            """
        )
        today_appointments = cursor.fetchone()[0]

        # Today's Revenue
        cursor.execute(
            """
            SELECT IFNULL(SUM(total_amount),0)
            FROM billing
            WHERE bill_date = DATE('now')
            """
        )
        today_revenue = cursor.fetchone()[0]

        conn.close()

        return {
            "users": total_users,
            "patients": total_patients,
            "medicines": total_medicines,
            "low_stock": low_stock,
            "expired": expired,
            "appointments": today_appointments,
            "revenue": today_revenue
        }