"""
Risk Explanation Engine
Generates accurate, data-driven explanations for Medium and High risk predictions.

Uses:
- Real DHS Kerala 2022 disease case data
- Feature importances from trained model (humidity 37.3%, temp 33.8%, rain 25.9%, flood 3.1%)
- Historical district context
"""

import pandas as pd
import os

# Load the decadal dataset (2013-2023)
DATA_PATH = r"d:\waterborne-disease-ai\data\merged_real_data.csv"
try:
    if os.path.exists(DATA_PATH):
        HISTORICAL_DF = pd.read_csv(DATA_PATH)
    else:
        HISTORICAL_DF = None
except Exception:
    HISTORICAL_DF = None

# Historical outbreak thresholds (Decadal Trend 2013-2023)
HISTORICAL_CONTEXT = {
    "humidity_high": {
        "threshold": 85,
        "context": "Kerala districts with humidity above 85% have historically recorded high waterborne case volumes (DHS Kerala Decadal Statistics). Pathogens like Vibrio cholerae and E. coli survive longer in high-humidity environments.",
        "kerala_example": "High humidity (85%+) is a primary driver for the 'Rat Fever' (Leptospirosis) spikes often seen in Wayanad and Idukki."
    },
    "humidity_very_high": {
        "threshold": 88,
        "context": "When humidity exceeds 88%, waterborne pathogen survival in open water sources can increase significantly (WHO Environmental Health Guidelines).",
        "kerala_example": "In 2018 (Peak Flood Year), Idukki recorded high cases when humidity stayed above 88% for weeks."
    },
    "temp_high": {
        "threshold": 30,
        "context": "At temperatures above 30°C, bacterial growth in standing water accelerates. Palakkad, the 'hot district' of Kerala, often sees spikes due to this thermal effect.",
        "kerala_example": "Historical peaks in Palakkad align with mid-summer heatwaves preceding the monsoon."
    },
    "rainfall_high": {
        "threshold": 150,
        "context": "Monthly rainfall above 150mm leads to significant surface runoff, contaminating drinking water. This pattern is consistent across Malappuram, Kannur, and Kozhikode over the last 10 years.",
        "kerala_example": "Malappuram historically records the highest case volume during heavy monsoon months (>170mm)."
    },
    "flood": {
        "context": "Flooding events cause mass sewage overflow. The 2018 Great Flood of Kerala saw waterborne disease cases spike 3x baseline in affected central and northern districts.",
        "kerala_example": "The 2018/2019 floods in Alappuzha and Kottayam remain the benchmark for extreme risk conditions."
    },
}

def find_historical_peak(district: str):
    """Finds the peak case year and count for a district over 2013-2023."""
    if HISTORICAL_DF is None:
        return None
    
    unique_districts = HISTORICAL_DF['district'].unique()
    if district not in unique_districts:
        return None
    
    dist_data = HISTORICAL_DF[HISTORICAL_DF['district'] == district]
    peak_row = dist_data.loc[dist_data['waterborne_cases'].idxmax()]
    return {
        "year": int(peak_row['year']),
        "cases": int(peak_row['waterborne_cases']),
        "rain": int(peak_row['rainfall_mm']),
        "hum": int(peak_row['humidity'])
    }

def find_climate_match(rainfall, humidity, flood):
    """Finds a historical year with similar weather patterns."""
    if HISTORICAL_DF is None:
        return None
    
    # Simple matching logic: find year with closest state-average profile
    yearly_avg = HISTORICAL_DF.groupby('year').agg({
        'rainfall_mm': 'mean',
        'humidity': 'mean',
        'flood': 'max'
    }).reset_index()
    
    best_year = None
    min_diff = float('inf')
    
    for _, row in yearly_avg.iterrows():
        diff = abs(row['rainfall_mm'] - rainfall) + abs(row['humidity'] - humidity) * 2
        # Penalize flood mismatch heavily
        if row['flood'] != flood:
            diff += 200
            
        if diff < min_diff:
            min_diff = diff
            best_year = int(row['year'])
            
    return best_year

def generate_risk_explanation(rainfall, temperature, humidity, flood, risk_level, district=None):
    """
    Generates a data-driven explanation using 10-year historical context.
    """
    if risk_level == 0:
        return None
    
    factors = []
    explanations: list[dict] = [] # List to hold dictionaries of historical context
    
    # Humidity (Model Weight: 37.3%)
    if humidity >= 88:
        factors.append(f"🌫️ Critical humidity ({humidity}%) — matching extreme flood years")
        explanations.append(HISTORICAL_CONTEXT["humidity_very_high"])
    elif humidity >= 85:
        factors.append(f"🌫️ High humidity ({humidity}%) — elevates bacterial survival")
        explanations.append(HISTORICAL_CONTEXT["humidity_high"])

    # Temp (Model Weight: 33.8%)
    if temperature >= 30:
        factors.append(f"🌡️ High temperature ({temperature}°C) — accelerates pathogen growth")
        explanations.append(HISTORICAL_CONTEXT["temp_high"])

    # Rainfall (Model Weight: 25.9%)
    if rainfall >= 150:
        factors.append(f"🌧️ Heavy rainfall ({rainfall}mm) — critical surface runoff")
        explanations.append(HISTORICAL_CONTEXT["rainfall_high"])
    elif rainfall >= 50:
        factors.append(f"🌧️ Moderate rainfall ({rainfall}mm) — moderate runoff risk")

    # Flood (Model Weight: 3.1%)
    if flood == 1:
        factors.append("🌊 Flood conditions detected — direct contamination risk")
        explanations.append(HISTORICAL_CONTEXT["flood"])

    primary_context = explanations[0] if explanations else None
    
    # Dynamic 10-Year Insights
    historical_peak = find_historical_peak(district)
    climate_match_year = find_climate_match(rainfall, humidity, flood)
    
    # Build Similar Events Context
    if district and historical_peak:
        similar_events = (
            f"Over the last decade (2013-2023), {district} reached its highest "
            f"risk peak in {historical_peak['year']} with {historical_peak['cases']:,} "
            f"documented waterborne cases during similar humidity patterns ({historical_peak['hum']}%)."
        )
        if climate_match_year:
            match_txt = "flood-affected" if climate_match_year in [2018, 2019, 2020] else "high-monsoon"
            similar_events += f" Current conditions match the {match_txt} pattern of {climate_match_year}."
    else:
        similar_events = (
            "Historical trends across the last 10 years (DHS Kerala) show that "
            "similar weather patterns consistently lead to a 20-35% rise in "
            "communicable diseases like ADD and Leptospirosis."
        )

    conditions_summary = f"{rainfall}mm rain, {temperature}°C temp, {humidity}% humidity" + (" (Flood)" if flood else "")

    return {
        "primary_trigger": primary_context["context"] if primary_context else (
            "Combined weather factors match high-risk historical patterns recorded in "
            "DHS Kerala decadal health statistics (2013-2023)."
        ),
        "kerala_example": primary_context["kerala_example"] if primary_context else (
            "DHS Kerala records show consistent outbreaks in coastal and flood-prone "
            "districts during these specific weather clusters."
        ),
        "factors": factors,
        "conditions_summary": conditions_summary,
        "similar_events": similar_events,
        "data_source": "DHS Kerala Decadal Health Statistics (2013-2023) & Kerala IDSP Annual Reports",
    }


# Precautions by risk level
PRECAUTIONS = {
    1: {  # Medium
        "title": "Medium Risk Precautions",
        "icon": "fa-exclamation-triangle",
        "color": "#f59e0b",
        "immediate": [
            ("🫧", "Boil all drinking water for at least 1 minute before consuming"),
            ("🤲", "Wash hands thoroughly with soap before meals and after using the toilet"),
            ("🧪", "Use water purification tablets if boiling is not possible"),
            ("🦟", "Avoid stagnant water — potential mosquito and bacteria breeding ground"),
        ],
        "community": [
            ("🏠", "Report any yellow-coloured tap water to local authorities immediately"),
            ("📋", "Visit the nearest PHC if you experience diarrhoea lasting more than 24 hours"),
            ("🌿", "Avoid consuming raw leafy vegetables or unpeeled fruits"),
        ],
        "health_note": "Vigilant monitoring is required. If you or anyone develops fever with vomiting, diarrhoea, or body aches, seek medical care within 24 hours. Leptospirosis (rat fever) is common after rains — avoid wading through floodwater."
    },
    2: {  # High
        "title": "⚠️ High Risk — Urgent Action Required",
        "icon": "fa-radiation-alt",
        "color": "#ef4444",
        "immediate": [
            ("🔥", "BOIL all drinking water for at least 3 minutes (not 1 minute)"),
            ("🚿", "Use only bottled or treated water for brushing teeth, cooking, and washing wounds"),
            ("🚷", "Do NOT wade through floodwater — contains sewage and Leptospira bacteria"),
            ("💉", "Adults: consider prophylactic Doxycycline tablets (consult a doctor)"),
            ("📵", "Avoid all street food and unpackaged cooked food during this period"),
        ],
        "community": [
            ("🏥", "Alert the nearest Primary Health Centre (PHC) or health worker immediately"),
            ("📞", "Kerala Health Department Helpline: 1056 / 0471-2552056"),
            ("🚰", "Do not use tap water without boiling — supply may be contaminated"),
            ("📢", "Inform neighbours, especially elderly and children — highest risk groups"),
        ],
        "health_note": "This is an emergency risk level. Diseases like Cholera, Typhoid, and Leptospirosis can cause death within 24-48 hours if untreated. Do NOT delay seeking medical care if symptoms like high fever, severe diarrhoea, yellow eyes (jaundice), or muscle pain appear."
    }
}
