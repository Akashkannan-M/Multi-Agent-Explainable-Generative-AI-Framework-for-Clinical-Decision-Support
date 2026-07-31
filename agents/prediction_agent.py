import pandas as pd
import joblib


class PredictionAgent:

    def __init__(self):

        self.model = joblib.load("models/disease_model.pkl")

        self.gender_encoder = joblib.load("models/gender_encoder.pkl")

        self.disease_encoder = joblib.load("models/disease_encoder.pkl")

    def predict(self, patient_data):

        patient_df = pd.DataFrame([patient_data])

        patient_df["Gender"] = self.gender_encoder.transform(
            patient_df["Gender"]
        )

        # Predict disease code
        prediction = self.model.predict(patient_df)

        # Convert code to disease name
        disease = self.disease_encoder.inverse_transform(prediction)

        # Get confidence scores
        probability = self.model.predict_proba(patient_df)

        confidence = round(max(probability[0]) * 100, 2)

        return disease[0], confidence