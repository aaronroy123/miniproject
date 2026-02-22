from model.predict import predict_risk

risk = predict_risk(
    rainfall=170,
    temperature=27,
    humidity=92,
    flood=1
)

print("Predicted Risk Level:", risk)
