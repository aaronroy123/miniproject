import pandas as pd

def load_and_merge(weather_path, disease_path):
    weather = pd.read_csv(weather_path)
    disease = pd.read_csv(disease_path)

    data = pd.merge(weather, disease, on=["date", "district"])

    def risk_label(cases):
        if cases < 30:
            return 0
        elif cases < 100:
            return 1
        else:
            return 2

    data["risk_level"] = data["waterborne_cases"].apply(risk_label)
    return data
