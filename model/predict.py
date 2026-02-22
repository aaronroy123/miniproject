import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "disease_risk_model.pkl")

model = joblib.load(MODEL_PATH)

FEATURES = ["rainfall_mm", "temperature", "humidity", "flood"]

def predict_risk(rainfall, temperature, humidity, flood):
    X = pd.DataFrame([[rainfall, temperature, humidity, flood]], columns=FEATURES)
    prediction = model.predict(X)[0]
    
    # Heuristic Override: Reduce false positives
    # If there is no rain and no flood, risk shouldn't be High just because of humidity
    if rainfall < 2.0 and flood == 0:
        if prediction == 2:  # Downgrade High to Medium
            return int(1)
        if prediction == 1 and humidity < 80: # Downgrade Medium to Low if not super humid
            return int(0)
            
    return int(prediction)
