import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from utils.preprocess import load_and_merge

# Load and preprocess data
data = load_and_merge(
    "data/raw_weather_data.csv",
    "data/disease_cases.csv"
)

# Features and target
X = data[["rainfall_mm", "temperature", "humidity", "flood"]]
y = data["risk_level"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print("Model Accuracy:", accuracy)

joblib.dump(model, "model/disease_risk_model.pkl")

print("Model saved successfully to D drive")
