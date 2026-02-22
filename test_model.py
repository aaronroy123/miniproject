import sys
import os
sys.path.append(os.getcwd())

from model.predict import predict_risk

print("Testing predict_risk...")
try:
    risk = predict_risk(10.0, 30.0, 80.0, 0)
    print(f"Risk: {risk}")
    print(f"Type: {type(risk)}")
except Exception as e:
    print(f"Error: {e}")
