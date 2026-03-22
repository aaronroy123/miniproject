import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "disease_risk_model.pkl")

model = joblib.load(MODEL_PATH)

# Features used during training (must match train_model_real.py)
FEATURES = ["rainfall_mm", "temperature", "humidity", "flood"]

# Risk label thresholds (based on 10-year Kerala DHS 2013-2023 dataset):
#   0 = Low    (< 25,000 annual waterborne cases per district)
#   1 = Medium (25,000 - 46,000 cases)
#   2 = High   (> 46,000 cases)

def predict_risk(rainfall, temperature, humidity, flood):
    X = pd.DataFrame([[rainfall, temperature, humidity, flood]], columns=FEATURES)
    prediction = model.predict(X)[0]
    
    # 1. High Humidity Sensitivity Booster (Clinical safety for tropical zones)
    # If humidity is high, it's rarely "safe" in Kerala even without rain.
    if humidity >= 80 and prediction == 0:
        prediction = 1
        
    # 2. Heuristic Override: Moderate false positives on extremely dry, non-flood days
    # Only downgrade if humidity is also low.
    if rainfall < 1.0 and flood == 0 and humidity < 75:
        if prediction == 2:  # Downgrade High to Medium
            return int(1)
        if prediction == 1:  # Downgrade Medium to Low
            return int(0)
            
    return int(prediction)
