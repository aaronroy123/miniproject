from utils.preprocess import load_and_merge

data = load_and_merge(
    "data/raw_weather_data.csv",
    "data/disease_cases.csv"
)

print("DATA SHAPE:", data.shape)
print(data)
