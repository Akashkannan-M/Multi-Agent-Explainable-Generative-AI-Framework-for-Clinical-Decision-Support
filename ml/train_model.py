import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load Dataset
df = pd.read_csv("dataset/clinical_decision_dataset.csv")

print(df.head())

# Remove Patient ID
df = df.drop("Patient_ID", axis=1)

# Create Encoders
gender_encoder = LabelEncoder()
disease_encoder = LabelEncoder()

# Encode Gender
df["Gender"] = gender_encoder.fit_transform(df["Gender"])

# Encode Disease
df["Disease"] = disease_encoder.fit_transform(df["Disease"])

# Features
X = df.drop("Disease", axis=1)

# Target
y = df["Disease"]

# Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train Model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Predict
prediction = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, prediction)

print("Accuracy :", accuracy)

# Save Model and Encoders
joblib.dump(model, "models/disease_model.pkl")
joblib.dump(gender_encoder, "models/gender_encoder.pkl")
joblib.dump(disease_encoder, "models/disease_encoder.pkl")

print("Model and Encoders Saved Successfully")