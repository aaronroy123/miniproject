"""
Updated Model Training Script — Uses REAL Kerala DHS + IMD Data
Training data: 12 Kerala districts, 2022, real disease case counts from DHS IDSP report
Weather: Based on documented 2022 Kerala district annual averages

Risk labels (data-driven tertiles based on real case distribution):
  0 = Low     (< 20,000 waterborne cases annually)
  1 = Medium  (20,000 - 43,000 cases)
  2 = High    (> 43,000 cases)
"""

import sys
import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, classification_report

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load real merged dataset
data = pd.read_csv("data/merged_real_data.csv")

print(f"Loaded {len(data)} real training records\n")

# Apply risk label using data-driven tertiles
def risk_label(cases):
    if cases < 20000:
        return 0   # Low     (~4 districts: Pathanamthitta, Idukki, Kollam, Kottayam)
    elif cases < 43000:
        return 1   # Medium  (~4 districts: Alappuzha, Thrissur, Wayanad, Palakkad)
    else:
        return 2   # High    (~4 districts: Thiruvananthapuram, Ernakulam, Kannur, Malappuram)

data["risk_level"] = data["waterborne_cases"].apply(risk_label)

print("\nRisk distribution:")
print(data.groupby("risk_level")[["district"]].count().rename(columns={"district": "count"}))
print("\nLabeled data:")
print(data[["district", "waterborne_cases", "risk_level"]])

# Features and target
FEATURES = ["rainfall_mm", "temperature", "humidity", "flood"]
X = data[FEATURES]
y = data["risk_level"]

# Since we only have 12 records, we use ALL data for training
# (train/test split is not meaningful with 12 rows - we use cross-validation instead)
print("\nTraining Random Forest on all 12 real records...")

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    max_depth=4  # Prevent overfitting on small dataset
)
model.fit(X, y)

# Cross-validation (better than train/test split for small datasets)
if len(data) >= 4:
    cv_scores = cross_val_score(model, X, y, cv=min(3, len(data)//2))
    print(f"\nCross-validation scores: {cv_scores}")
    print(f"Average CV accuracy: {cv_scores.mean():.2f}")

# Verify predictions
y_pred = model.predict(X)
print(f"\nTraining accuracy: {accuracy_score(y, y_pred):.2f}")
print("\nClassification report:")
print(classification_report(y, y_pred, zero_division=0))

# Feature importance
importance = pd.Series(model.feature_importances_, index=FEATURES).sort_values(ascending=False)
print("\nFeature Importances:")
for feat, imp in importance.items():
    print(f"  {feat}: {imp:.3f}")

# Save model
joblib.dump(model, "model/disease_risk_model.pkl")
print("\n✅ Model retrained with REAL DHS Kerala data and saved to model/disease_risk_model.pkl")
print("   Now using authentic 2022 district-wise waterborne disease statistics!")
