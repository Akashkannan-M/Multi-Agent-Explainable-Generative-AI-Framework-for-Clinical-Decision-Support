from agents.prediction_agent import PredictionAgent

agent = PredictionAgent()

patient = {
    "Age": 25,
    "Gender": "Male",
    "Fever": 1,
    "Cough": 1,
    "Headache": 1,
    "Fatigue": 1,
    "Chest_Pain": 0,
    "Shortness_of_Breath": 0,
    "Sore_Throat": 1,
    "Vomiting": 0,
    "Diarrhea": 0,
    "Joint_Pain": 0,
    "Itching": 0,
    "Redness": 0,
    "Swelling": 0,
    "Dry_Skin": 0,
    "Burning": 0,
    "Rash": 0,
    "Pain": 0,
    "Family_History": 0
}

result = agent.predict(patient)

print("Predicted Disease :", result)