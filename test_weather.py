from flask import Flask, jsonify
from utils.weather import get_weather_data

app = Flask(__name__)

@app.route("/")
def home():
    return "<h2>AI Waterborne Disease System Backend is Running</h2>"

@app.route("/weather")
def weather():
    rainfall, temperature, humidity, flood = get_weather_data("Kottayam")

    return jsonify({
        "rainfall": rainfall,
        "temperature": temperature,
        "humidity": humidity,
        "flood": flood
    })

if __name__ == "__main__":
    app.run(debug=True)
