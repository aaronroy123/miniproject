import requests
import math

API_KEY = "99f4eb76222a2cc563236ca49f390cfa"  # paste exactly, no spaces

def calculate_dew_point(temp, humidity):
    """
    Calculate Dew Point using the simple approximation:
    T_dp = T - ((100 - RH)/5)
    """
    return round(temp - ((100 - humidity) / 5), 1)

def get_weather_data(city):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)
    data = response.json()

    # Handle API errors safely
    if "main" not in data:
        raise Exception(f"Weather API error: {data}")

    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    rainfall = data.get("rain", {}).get("1h", 0)
    visibility = data.get("visibility", 10000) / 1000 # Convert to km
    wind_speed = data.get("wind", {}).get("speed", 0)
    wind_deg = data.get("wind", {}).get("deg", 0)
    
    dew_point = calculate_dew_point(temperature, humidity)

    # Flood logic
    flood = 1 if rainfall > 150 else 0

    return {
        "rainfall": rainfall,
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure,
        "visibility": round(visibility, 1),
        "wind_speed": wind_speed,
        "wind_deg": wind_deg,
        "dew_point": dew_point,
        "flood": flood,
        "description": data["weather"][0]["description"].title() if data.get("weather") else "Unknown"
    }

def search_cities(query):
    """
    Search for cities using OpenWeatherMap Geocoding API.
    Returns a list of dicts with name, country, state.
    """
    limit = 5
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={query}&limit={limit}&appid={API_KEY}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def get_weather_by_coords(lat, lon):
    """
    Fetch weather data by latitude and longitude.
    """
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    )

    try:
        response = requests.get(url)
        data = response.json()

        if "main" not in data:
            return None

        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        rainfall = data.get("rain", {}).get("1h", 0)
        visibility = data.get("visibility", 10000) / 1000 # km
        wind_speed = data.get("wind", {}).get("speed", 0)
        wind_deg = data.get("wind", {}).get("deg", 0)
        
        dew_point = calculate_dew_point(temperature, humidity)
        
        # Flood logic
        flood = 1 if rainfall > 150 else 0
        
        return {
            "name": data.get("name", "Unknown Location"),
            "temp": temperature, # standardizing to 'temperature' in next refactor might be better, but keeping 'temp' for now to match frontend if needed, actually let's standardize to 'temperature' in the object but 'temp' might be used by JS. Let's check app.py usage.
            # actually app.py passes this dict directly to frontend in one case, and extracts values in another.
            # Let's align keys with get_weather_data for consistency.
            "temperature": temperature, 
            "humidity": humidity,
            "pressure": pressure,
            "visibility": round(visibility, 1),
            "wind_speed": wind_speed,
            "wind_deg": wind_deg,
            "dew_point": dew_point,
            "rainfall": rainfall,
            "flood": flood,
            "description": data["weather"][0]["description"].title() if data.get("weather") else "Unknown"
        }
    except:
        return None
