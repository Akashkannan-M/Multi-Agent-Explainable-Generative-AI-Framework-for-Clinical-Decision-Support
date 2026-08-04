import os
import streamlit as st
import matplotlib.pyplot as plt

from agents.prediction_agent import PredictionAgent
from agents.patient_agent import PatientAgent
from agents.recommendation_agent import RecommendationAgent
from agents.report_agent import ReportAgent
from agents.explanation_agent import ExplanationAgent
from agents.genai_agent import GenAIAgent
from agents.history_agent import HistoryAgent
from agents.dashboard_agent import DashboardAgent
from agents.auth_agent import AuthAgent 
from agents.user_agent import UserAgent
from agents.report_history_agent import ReportHistoryAgent
from agents.image_agent import ImageAgent
from agents.shap_agent import SHAPAgent
from agents.chatbot_agent import ChatbotAgent
from agents.chat_history_agent import ChatHistoryAgent
from agents.appointment_agent import AppointmentAgent
from agents.prescription_agent import PrescriptionAgent
from agents.medicine_agent import MedicineAgent
from agents.invoice_agent import InvoiceAgent
from agents.analytics_agent import AnalyticsAgent
from agents.admin_dashboard_agent import AdminDashboardAgent
from agents.doctor_analytics_agent import DoctorAnalyticsAgent
# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Clinical Decision Support",
    page_icon="🏥",
    layout="wide"
)

# --------------------------------------------------
# Initialize Agents
# --------------------------------------------------

prediction_agent = PredictionAgent()
patient_agent = PatientAgent()
recommendation_agent = RecommendationAgent()
report_agent = ReportAgent()
explanation_agent = ExplanationAgent()
genai_agent = GenAIAgent()
history_agent = HistoryAgent()
dashboard_agent = DashboardAgent()
auth_agent = AuthAgent()
user_agent = UserAgent()
report_history_agent = ReportHistoryAgent()
image_agent = ImageAgent()
shap_agent = SHAPAgent()
chatbot_agent = ChatbotAgent()
chat_history_agent = ChatHistoryAgent()
appointment_agent = AppointmentAgent()
prescription_agent = PrescriptionAgent()
medicine_agent = MedicineAgent()
invoice_agent = InvoiceAgent()
analytics_agent = AnalyticsAgent()
admin_dashboard_agent = AdminDashboardAgent()
doctor_analytics_agent = DoctorAnalyticsAgent()
# ==========================================
# Login
# ==========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("🔐 Clinical Decision Support Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        user = auth_agent.login(username, password)

        if user:
            st.session_state.logged_in = True
            st.session_state.username = user[1]
            st.session_state.role = user[3]

            st.success("Login Successful!")
            st.rerun()

        else:
            st.error("Invalid Username or Password.")

    st.stop()

# --------------------------------------------------
# Sidebar
# --------------------------------------------------




if st.session_state.role == "Admin":

    page = st.sidebar.selectbox(
        "Menu",
        [
            "Disease Prediction",
            "Patient History",
            "Dashboard",
            "User Management",
            "Reports",
            "AI Chatbot",
            "Chat History",
            "Appointments",
            "Prescriptions",
            "Medicine Inventory",
            "Admin Dashboard",
            "Doctor Analytics"
        ]
    )

elif st.session_state.role == "Patient":

    page = st.sidebar.selectbox(
        "Patient Menu",
        [
            "🏠 Home",
            "👤 My Profile",
            "📋 My Medical History",
            "📄 My Reports",
            "💬 AI Medical Chatbot",
            "📅 Book Appointment",
            "💊 My Prescriptions"
        ]
    )


elif st.session_state.role == "Doctor":

    page = st.sidebar.selectbox(
        "Menu",
        [
            "Disease Prediction",
            "Patient History",
            "Dashboard",
            "Reports",
            "AI Chatbot",
            "Chat History",
            "Appointments",
            "Prescriptions",
            "Medicine Inventory",
            
        ]
    )

else:
    st.error("Unauthorized User")
    st.stop()
    
st.sidebar.divider()

if st.sidebar.button("🚪 Logout"):

    st.session_state.logged_in = False
    st.session_state.clear()

    st.rerun()
    




# ==================================================
# DASHBOARD
# ==================================================

if page == "Dashboard":

    data = dashboard_agent.get_dashboard()

    left, right = st.columns([3, 1])

    with left:

        st.title("📊 Clinical Dashboard")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("👨‍⚕️ Patients", data["patients"])
        col2.metric("🦠 Diseases", data["diseases"])
        col3.metric("👨 Male", data["male"])
        col4.metric("👩 Female", data["female"])

        st.metric("🏥 Most Common Disease", data["common"])

        st.divider()

        st.subheader("📊 Hospital Analytics")

        total_patients = analytics_agent.total_patients()
        today_patients = analytics_agent.today_patients()
        monthly_revenue = analytics_agent.monthly_revenue()

        a1, a2, a3 = st.columns(3)

        with a1:
            st.metric("Total Patients", total_patients)

        with a2:
            st.metric("Today's Patients", today_patients)

        with a3:
            st.metric("Monthly Revenue", f"₹{monthly_revenue:.2f}")

    with right:

        st.subheader("🦠 Disease Statistics")

        disease_df = analytics_agent.disease_statistics()

        if not disease_df.empty:

            fig, ax = plt.subplots(figsize=(3,3))

            ax.bar(
                disease_df["disease"].astype(str),
                disease_df["Total"].astype(int)
            )

            ax.set_xlabel("")
            ax.set_ylabel("")

            plt.xticks(rotation=45, fontsize=8)

            st.pyplot(fig)

        else:
            st.info("No Data")

    st.divider()

    # =====================================
    # Filter Patients by Date
    # =====================================

    st.subheader("📅 Filter Patients by Date")

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("Start Date")

    with col2:
        end_date = st.date_input("End Date")

    if st.button("Filter Records"):

        filtered = dashboard_agent.filter_by_date(
            str(start_date),
            str(end_date)
        )

        st.dataframe(filtered, use_container_width=True)

    st.stop()
    
    
# ==================================================
# PATIENT HISTORY
# ==================================================

if page == "Patient History":

    st.title("📋 Patient History")

    search = st.text_input("🔍 Search Patient")

    if search:
        df = history_agent.search_patient(search)
    else:
        df = history_agent.get_patients()

    st.dataframe(df, use_container_width=True)

    # -----------------------------
    # Delete Patient
    # -----------------------------

    st.divider()

    patient_id = st.number_input(
        "Enter Patient ID to Delete",
        min_value=1,
        step=1
    )

    if st.button("🗑 Delete Patient"):

        history_agent.delete_patient(patient_id)

        st.success("Patient deleted successfully.")

        st.rerun()

    # -----------------------------
    # Update Patient
    # -----------------------------

    st.divider()

    st.subheader("✏️ Update Patient")

    update_id = st.number_input(
        "Patient ID",
        min_value=1,
        step=1,
        key="update_id"
    )

    new_name = st.text_input("New Name")

    new_age = st.number_input(
        "New Age",
        min_value=1,
        max_value=120,
        value=25,
        key="new_age"
    )

    new_gender = st.selectbox(
        "New Gender",
        ["Male", "Female"]
    )

    new_disease = st.text_input("New Disease")

    if st.button("✏️ Update Patient"):

        history_agent.update_patient(
            update_id,
            new_name,
            new_age,
            new_gender,
            new_disease
        )

        st.success("Patient updated successfully.")

        st.rerun()

    # -----------------------------
    # Excel Download
    # -----------------------------

    st.divider()

    excel_file = history_agent.export_excel()

    with open(excel_file, "rb") as file:

        st.download_button(
            label="📥 Download Patient History (Excel)",
            data=file,
            file_name="Patient_History.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    st.stop()

#-----------
#User Management
#----------  

if page == "User Management":

    st.title("👨‍⚕️ User Management")

    st.metric("Total Users", user_agent.total_users())

    st.divider()

    search = st.text_input("Search Username")

    if search:
        df = user_agent.search_user(search)
    else:
        df = user_agent.get_users()

    st.dataframe(df, use_container_width=True)

    st.divider()

    st.subheader("➕ Add New User")

    username = st.text_input("Username")

    password = st.text_input("Password")

    role = st.selectbox(
        "Role",
        ["Admin", "Doctor", "Patient"]
    )

    if st.button("Add User"):

        user_agent.add_user(
            username,
            password,
            role
        )

        st.success("User Added Successfully")

        st.rerun()

    st.divider()

    st.subheader("🗑 Delete User")

    user_id = st.number_input(
        "User ID",
        min_value=1,
        step=1
    )

    if st.button("Delete User"):

        user_agent.delete_user(user_id)

        st.success("User Deleted Successfully")

        st.rerun()

    st.stop()


# ==================================================
# REPORTS
# ==================================================

if page == "Reports":

    st.title("📄 Clinical Prediction Reports")
    st.write("View and download all patient prediction reports.")

    st.divider()

    # ----------------------------
    # Filter
    # ----------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        start_date = st.date_input("📅 Start Date")

    with col2:
        end_date = st.date_input("📅 End Date")

    with col3:
        search = st.text_input("🔍 Search Patient")

    if st.button("Search Reports"):

        df = report_history_agent.filter_reports(
            str(start_date),
            str(end_date)
        )

        if search.strip():
            df = df[df["name"].str.contains(search, case=False)]

    else:
        df = report_history_agent.get_reports()

    st.divider()

    st.subheader("📋 Report List")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ----------------------------
    # Statistics
    # ----------------------------

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Total Reports", len(df))

    with c2:
        if not df.empty:
            st.metric("Diseases", df["disease"].nunique())
        else:
            st.metric("Diseases", 0)

    with c3:
        if not df.empty:
            st.metric("Latest Report", df.iloc[-1]["prediction_date"])
        else:
            st.metric("Latest Report", "-")

    st.divider()

    # ----------------------------
    # Download CSV
    # ----------------------------

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Reports (CSV)",
        data=csv,
        file_name="Clinical_Reports.csv",
        mime="text/csv"
    )

    st.stop()
# ==================================================
# CHAT HISTORY
# ==================================================

if page == "Chat History":

    st.title("💬 Chat History")

    df = chat_history_agent.get_history()

    st.dataframe(df, use_container_width=True)

    st.stop()
    
# ==================================================
# APPOINTMENTS
# ==================================================

if page == "Appointments":

    st.title("📅 Doctor Appointment Management")

    st.subheader("Book Appointment")

    patient_name = st.text_input("Patient Name")

    doctor_name = st.text_input("Doctor Name")

    appointment_date = st.date_input("Appointment Date")

    appointment_time = st.time_input("Appointment Time")

    if st.button("Book Appointment"):

        appointment_agent.book_appointment(
            patient_name,
            doctor_name,
            str(appointment_date),
            str(appointment_time)
        )

        st.success("Appointment Booked Successfully")

        st.rerun()

    st.divider()

    st.subheader("Appointment List")

    df = appointment_agent.get_appointments()

    st.dataframe(df, use_container_width=True)

    
    
    st.divider()

    st.subheader("Update Appointment Status")

    appointment_id = st.number_input(
        "Appointment ID",
        min_value=1,
        step=1
    )

    status = st.selectbox(
        "Select Status",
        [
            "Pending",
            "Approved",
            "Completed"
        ]
    )

    if st.button("Update Status"):
        appointment_agent.update_status(
            appointment_id,
            status
        )

        st.success("Appointment Status Updated Successfully")

        st.rerun()
    
    st.stop()

# ==================================================
# PRESCRIPTIONS
# ==================================================

if page == "Prescriptions":

    st.title("💊 Prescription Management")

    patient_name = st.text_input("Patient Name")

    doctor_name = st.text_input("Doctor Name")

    diagnosis = st.text_area("Diagnosis")

    medicines = st.text_area("Medicines")

    dosage = st.text_area("Dosage")

    advice = st.text_area("Advice")

    prescription_date = st.date_input("Prescription Date")

    if st.button("Save Prescription"):

        prescription_agent.add_prescription(
            patient_name,
            doctor_name,
            diagnosis,
            medicines,
            dosage,
            advice,
            str(prescription_date)
        )

        st.success("Prescription Saved Successfully")

        st.rerun()

    st.divider()

    st.subheader("Prescription History")

    df = prescription_agent.get_prescriptions()

    st.dataframe(df, use_container_width=True)

    st.stop()
    
# ==================================================
# MEDICINE INVENTORY
# ==================================================

if page == "Medicine Inventory":

    st.title("💊 Medicine Inventory Management")

    medicine_name = st.text_input("Medicine Name")

    quantity = st.number_input(
        "Quantity",
        min_value=0,
        step=1
    )

    expiry_date = st.date_input("Expiry Date")

    manufacturer = st.text_input("Manufacturer")

    if st.button("Add Medicine"):

        medicine_agent.add_medicine(
            medicine_name,
            quantity,
            str(expiry_date),
            manufacturer
        )

        st.success("Medicine Added Successfully")

        st.rerun()

    st.divider()

    st.subheader("Medicine Stock")

    df = medicine_agent.get_medicines()

    st.dataframe(df, use_container_width=True)
    
    st.divider()

    st.subheader("⚠️ Low Stock Medicines")

    low_stock = medicine_agent.low_stock()

    if not low_stock.empty:
        st.warning("Low Stock Medicines Found")
        st.dataframe(low_stock, use_container_width=True)
    else:
        st.success("No Low Stock Medicines")


    st.divider()

    st.subheader("⏰ Expired Medicines")

    expired = medicine_agent.expired_medicines()

    if not expired.empty:
        st.error("Expired Medicines Found")
        st.dataframe(expired, use_container_width=True)
    else:
        st.success("No Expired Medicines")

    st.stop()


    
# ==================================================
# ADMIN DASHBOARD
# ==================================================

if page == "Admin Dashboard":

    st.title("🏥 Live Hospital Monitoring Dashboard")

    data = admin_dashboard_agent.get_dashboard()

    col1, col2, col3 = st.columns(3)

    col1.metric("👥 Total Users", data["users"])
    col2.metric("👨‍⚕️ Patients", data["patients"])
    col3.metric("💊 Medicines", data["medicines"])

    st.divider()

    col4, col5, col6 = st.columns(3)

    col4.metric("⚠️ Low Stock", data["low_stock"])
    col5.metric("⏰ Expired Medicines", data["expired"])
    col6.metric("📅 Today's Appointments", data["appointments"])

    st.divider()

    st.metric("💰 Today's Revenue", f"₹{data['revenue']:.2f}")

    st.stop() 
    
    
# ==================================================
# DOCTOR ANALYTICS
# ==================================================

if page == "Doctor Analytics":

    st.title("👨‍⚕️ Doctor Analytics")

    # ---------------------------------
    # Doctor Patient Count
    # ---------------------------------

    st.subheader("👨‍⚕️ Patients Handled by Doctors")

    patient_df = doctor_analytics_agent.doctor_patient_count()

    st.dataframe(patient_df, use_container_width=True)

    st.divider()

    # ---------------------------------
    # Doctor Specialization
    # ---------------------------------

    st.subheader("🩺 Doctor Specialization")

    specialization_df = doctor_analytics_agent.doctor_specialization()

    st.dataframe(specialization_df, use_container_width=True)

    st.divider()

    # ---------------------------------
    # Patient Treatment History
    # ---------------------------------

    st.subheader("💊 Patient Treatment History")

    treatment_df = doctor_analytics_agent.patient_treatment_history()

    st.dataframe(treatment_df, use_container_width=True)

    st.stop()


# ==================================================
# PATIENT HOME
# ==================================================

if page == "🏠 Home":

    st.title("🏥 Patient Dashboard")

    st.success(
        f"Welcome {st.session_state.username}"
    )

    # Report Count
    reports = report_history_agent.patient_report_count(
        st.session_state.username
    )

    # Appointment Count
    appointments = appointment_agent.patient_appointment_count(
        st.session_state.username
    )

    # Prescription Count
    prescriptions = prescription_agent.patient_prescription_count(
        st.session_state.username
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "📄 My Reports",
        reports
    )

    col2.metric(
        "📅 My Appointments",
        appointments
    )

    col3.metric(
        "💊 My Prescriptions",
        prescriptions
    )

    st.divider()

    st.info(
        "View your medical history, reports, appointments and prescriptions from the sidebar."
    )


# ==================================================
# MY PROFILE
# ==================================================

if page == "👤 My Profile":

    st.title("👤 Patient Profile")

    col1, col2 = st.columns(2)


    with col1:

        st.text_input(
            "Patient Name",
            value=st.session_state.username
        )

        st.number_input(
            "Age",
            value=25
        )


    with col2:

        st.selectbox(
            "Gender",
            [
                "Male",
                "Female"
            ]
        )


        st.text_input(
            "Blood Group",
            "O+"
        )


    st.text_input(
        "Phone Number"
    )

    st.text_input(
        "Email"
    )


    if st.button("Update Profile"):

        st.success(
            "Profile Updated Successfully"
        )


    st.stop()



# ==================================================
# MY MEDICAL HISTORY
# ==================================================

if page == "📋 My Medical History":

    st.title("📋 Medical History")


    df = history_agent.patient_history(
        st.session_state.username
    )


    if not df.empty:

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.info(
            "No Medical Records Found"
        )


    st.stop()



# ==================================================
# MY REPORTS
# ==================================================

if page == "📄 My Reports":

    st.title("📄 My Medical Reports")


    reports = report_history_agent.get_reports(
        st.session_state.username
    )


    if not reports.empty:

        st.dataframe(
            reports,
            use_container_width=True
        )


    else:

        st.info(
            "No Reports Available"
        )


    st.stop()



# ==================================================
# AI MEDICAL CHATBOT
# ==================================================

if page == "💬 AI Medical Chatbot":


    st.title(
        "🤖 AI Health Assistant"
    )


    question = st.text_area(
        "Ask your health related question"
    )


    if st.button("Ask AI"):


        if question.strip():

            response = chatbot_agent.reply(
                question
            )

            st.success(response)


            chat_history_agent.save_chat(
                question,
                response
            )


        else:

            st.warning(
                "Please enter your question"
            )


    st.stop()



# ==================================================
# BOOK APPOINTMENT
# ==================================================

if page == "📅 Book Appointment":


    st.title(
        "📅 Doctor Appointment"
    )


    doctor = st.selectbox(
        "Select Doctor",
        [
            "Dr. John",
            "Dr. Kumar",
            "Dr. Priya"
        ]
    )


    appointment_date = st.date_input(
        "Appointment Date"
    )


    reason = st.text_area(
        "Reason for Visit"
    )


    if st.button("Book Appointment"):


        appointment_agent.book_appointment(
            st.session_state.username,
            doctor,
            str(appointment_date),
            reason
        )


        st.success(
            "Appointment Booked Successfully"
        )


    st.divider()


    st.subheader(
        "My Appointments"
    )


    st.dataframe(
        appointment_agent.get_appointments(
            st.session_state.username
        ),
        use_container_width=True
    )


    st.stop()



# ==================================================
# MY PRESCRIPTIONS
# ==================================================

if page == "💊 My Prescriptions":


    st.title(
        "💊 My Prescriptions"
    )


    prescriptions = prescription_agent.get_prescriptions(
        st.session_state.username
    )


    if not prescriptions.empty:


        st.dataframe(
            prescriptions,
            use_container_width=True
        )


    else:

        st.info(
            "No Prescriptions Found"
        )


    st.stop()
     
# ==================================================
# DISEASE PREDICTION
# ==================================================

st.title("🏥 Multi-Agent Clinical Decision Support System")

st.write("Welcome to the AI-based Clinical Decision Support System.")

st.divider()


# --------------------------------------------------
# Patient Information
# --------------------------------------------------

st.header("Patient Information")

name = st.text_input("Patient Name")

age = st.number_input(
    "Age",
    min_value=1,
    max_value=120,
    value=25
)

gender = st.selectbox(
    "Gender",
    ["Male", "Female"]
)

doctor_name = st.selectbox(
    "Doctor",
    [
        "Dr. John",
        "Dr. Kumar",
        "Dr. Priya"
    ]
)


#----------------
# IMAGE SYMPTOMS
#----------------

st.divider()

st.subheader("🖼 Upload Medical Image")

uploaded_file = st.file_uploader(
    "Upload Medical Image (Optional)",
    type=["jpg", "jpeg", "png"]
)

image_result = "No Medical Image Uploaded"

if uploaded_file is not None:
    image_result = image_agent.analyze_image(uploaded_file.name)

# --------------------------------------------------
# Symptoms
# --------------------------------------------------

st.header("Symptoms")

fever = st.checkbox("Fever")
cough = st.checkbox("Cough")
headache = st.checkbox("Headache")
fatigue = st.checkbox("Fatigue")
chest_pain = st.checkbox("Chest Pain")
shortness_of_breath = st.checkbox("Shortness of Breath")
sore_throat = st.checkbox("Sore Throat")
vomiting = st.checkbox("Vomiting")
diarrhea = st.checkbox("Diarrhea")
joint_pain = st.checkbox("Joint Pain")
itching = st.checkbox("Itching")
redness = st.checkbox("Redness")
swelling = st.checkbox("Swelling")
dry_skin = st.checkbox("Dry Skin")
burning = st.checkbox("Burning")
rash = st.checkbox("Rash")
pain = st.checkbox("Pain")
family_history = st.checkbox("Family History")

st.subheader("Additional Symptoms")

extra_symptoms = st.text_area(
    "Enter Extra Symptoms (comma separated)",
    placeholder="Example: nausea, dizziness, body pain"
)

# --------------------------------------------------
# Predict
# --------------------------------------------------

if st.button("🔍 Predict Disease"):

    patient = {
        "Age": age,
        "Gender": gender,
        "Fever": int(fever),
        "Cough": int(cough),
        "Headache": int(headache),
        "Fatigue": int(fatigue),
        "Chest_Pain": int(chest_pain),
        "Shortness_of_Breath": int(shortness_of_breath),
        "Sore_Throat": int(sore_throat),
        "Vomiting": int(vomiting),
        "Diarrhea": int(diarrhea),
        "Joint_Pain": int(joint_pain),
        "Itching": int(itching),
        "Redness": int(redness),
        "Swelling": int(swelling),
        "Dry_Skin": int(dry_skin),
        "Burning": int(burning),
        "Rash": int(rash),
        "Pain": int(pain),
        "Family_History": int(family_history)
    }

    # Predict Disease (Internal)
    disease, confidence = prediction_agent.predict(patient)

    # Save Patient
    patient_agent.save_patient(
        name,
        age,
        gender,
        disease,
        doctor_name
    )

    st.success("Patient record saved successfully.")

    # Additional Symptoms
    if extra_symptoms.strip():

        st.subheader("Additional Symptoms")

        symptom_list = [
            symptom.strip()
            for symptom in extra_symptoms.split(",")
            if symptom.strip()
        ]

        for symptom in symptom_list:
            st.write("✅", symptom)

    # Image Analysis
    if uploaded_file is not None:
        st.subheader("🖼 Image Analysis")
        st.info(image_result)

    # Recommendations
    recommendations = recommendation_agent.get_recommendation(disease)

    st.subheader("📋 Recommendations")

    for item in recommendations:
        st.write("✅", item)

    # Explainable Reasons
    reasons = explanation_agent.explain(patient)

    st.subheader("🧠 Why was this disease predicted?")

    for reason in reasons:
        st.write("🔹", reason)

    # AI Explanation
    ai_response = genai_agent.generate_response(
        disease,
        confidence,
        recommendations
    )

    st.subheader("🤖 AI Clinical Explanation")
    st.write(ai_response)

    # PDF Report
    pdf_file = report_agent.generate_report(
        name,
        age,
        gender,
        disease,
        confidence,
        recommendations,
        image_result
    )

    st.success("PDF Report Generated Successfully")

    with open(pdf_file, "rb") as pdf:

        st.download_button(
            label="📄 Download PDF Report",
            data=pdf,
            file_name=os.path.basename(pdf_file),
            mime="application/pdf"
        )