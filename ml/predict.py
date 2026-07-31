import pandas as pd
import joblib

# Load Model
model = joblib.load("models/disease_model.pkl")

# Load Encoders
gender_encoder = joblib.load("models/gender_encoder.pkl")
disease_encoder = joblib.load("models/disease_encoder.pkl")

# Patient Details
patient = {
    "Age": [25],
    "Gender": ["Male"],
    "Fever": [1],
    "Cough": [1],
    "Headache": [1],
    "Fatigue": [1],
    "Chest_Pain": [0],
    "Shortness_of_Breath": [0],
    "Sore_Throat": [1],
    "Vomiting": [0],
    "Diarrhea": [0],
    "Joint_Pain": [0],
    "Itching": [0],
    "Redness": [0],
    "Swelling": [0],
    "Dry_Skin": [0],
    "Burning": [0],
    "Rash": [0],
    "Pain": [0],
    "Family_History": [0]
}

# Convert to DataFrame
patient_df = pd.DataFrame(patient)

# Convert Gender into Number
patient_df["Gender"] = gender_encoder.transform(patient_df["Gender"])

# Predict Disease
prediction = model.predict(patient_df)

# Convert Number back to Disease Name
disease_name = disease_encoder.inverse_transform(prediction)

print("Predicted Disease :", disease_name[0])