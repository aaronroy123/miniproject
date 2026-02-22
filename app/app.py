import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, session, redirect, url_for
from model.predict import predict_risk
from utils.weather import get_weather_data, search_cities, get_weather_by_coords

app = Flask(__name__)
app.secret_key = "super_secret_secure_key_2026"  # In production, use enc vars

# Kerala district → city mapping
DISTRICTS = {
    "Alappuzha": "Alappuzha",
    "Ernakulam": "Kochi",
    "Idukki": "Idukki",
    "Kannur": "Kannur",
    "Kasaragod": "Kasaragod",
    "Kollam": "Kollam",
    "Kottayam": "Kottayam",
    "Kozhikode": "Kozhikode",
    "Malappuram": "Malappuram",
    "Palakkad": "Palakkad",
    "Pathanamthitta": "Pathanamthitta",
    "Thiruvananthapuram": "Thiruvananthapuram",
    "Thrissur": "Thrissur",
    "Wayanad": "Wayanad"
}

@app.route("/", methods=["GET", "POST"])
def dashboard():
    weather = None
    message = None
    selected_district = None

    if request.method == "POST":
        user_input = request.form.get("district")
        
        # Try to map district to city if it's in our Kerala list, otherwise use input as is
        city = DISTRICTS.get(user_input, user_input)

        if not city:
            return render_template(
                "dashboard.html",
                districts=list(DISTRICTS.keys()),
                selected_district=None,
                weather=None,
                message="Please enter a valid city name."
            )
        
        try:
            # New: returns a dict
            weather_data = get_weather_data(city)
            
            risk = predict_risk(
                weather_data["rainfall"], 
                weather_data["temperature"], 
                weather_data["humidity"], 
                weather_data["flood"]
            )

            # Pass the full dict to the template
            weather = weather_data
            weather["risk"] = risk # Add risk to the object for template use if needed

            if risk == 0:
                message = "LOW RISK: Situation is safe."
            elif risk == 1:
                message = "MEDIUM RISK: Monitor water quality."
            else:
                message = "HIGH RISK: Immediate preventive action required!"
        except Exception as e:
            return render_template(
                "dashboard.html",
                districts=list(DISTRICTS.keys()),
                selected_district=None,
                weather=None,
                message=f"Error fetching data: {str(e)}"
            )

    return render_template(
        "dashboard.html",
        districts=list(DISTRICTS.keys()),
        selected_district=selected_district,
        weather=weather,
        message=message
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Hardcoded admin credentials (demo purpose)
        if username == "admin" and password == "admin123":
            session["user"] = "admin"
            return redirect(url_for("admin_dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials. Access denied.")
            
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/admin")
def admin_dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
        
    # Generate district-wise risk data using REAL data
    district_data = []
    
    # We use a subset or fetch all, depending on performance. 
    # For now, let's fetch real data for all 14 districts.
    for district, city in DISTRICTS.items():
        try:
            w = get_weather_data(city)
            risk_score = predict_risk(w["rainfall"], w["temperature"], w["humidity"], w["flood"])
            
            risk_label = "Low" if risk_score == 0 else "Medium" if risk_score == 1 else "High"
            
            # Simple trend simulation based on rainfall
            if w["rainfall"] > 10:
                trend = "Rising"
            elif w["rainfall"] > 0:
                trend = "Stable"
            else:
                trend = "Falling"
                
            cases = int(w["rainfall"] * 0.5) # Simulate cases correlated with rain
            
        except:
            # Fallback if API fails
            risk_label = "Unknown"
            trend = "Stable"
            cases = 0
        
        district_data.append({
            "name": district,
            "risk": risk_label,
            "trend": trend,
            "cases": cases
        })
        
    return render_template("admin.html", district_data=district_data)

@app.route("/api/history")
def get_history_data():
    # Mock historical data for charts
    import random
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    rainfall = [random.randint(50, 300) for _ in range(12)]
    risk_level = [random.randint(10, 90) for _ in range(12)]
    
    return {
        "labels": months,
        "rainfall": rainfall,
        "risk": risk_level
    }

@app.route("/api/risk_map")
def get_risk_map_data():
    # Mock risk data for all districts for the map - NOW USING REAL DATA
    district_risks = {}
    for district, city in DISTRICTS.items():
        try:
            w = get_weather_data(city)
            risk_score = predict_risk(w["rainfall"], w["temperature"], w["humidity"], w["flood"])
            district_risks[district] = risk_score
        except:
            district_risks[district] = 0 # Default to Low if API fails
        
    return district_risks

@app.route("/api/search_cities")
def api_search_cities():
    query = request.args.get("q", "")
    if not query:
        return {"results": []}
    
    results = search_cities(query)
    return {"results": results}

@app.route("/api/weather_coords")
def api_weather_coords():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    
    if not lat or not lon:
        return {"error": "Missing coordinates"}, 400
        
    data = get_weather_by_coords(lat, lon)
    
    if not data:
        return {"error": "Weather data not found"}, 404
        
    # Calculate risk on the fly
    risk = predict_risk(data["rainfall"], data["temperature"], data["humidity"], data["flood"])
    data["risk"] = risk
    
    return data

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
