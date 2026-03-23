# Detailed Project Description: AI Waterborne Disease Early Warning System

This document provides an exhaustive technical breakdown of the Waterborne Disease AI project, detailing every tool, dataset, and methodology used in its development.

---

## 1. Project Overview
The **AI Waterborne Disease Early Warning System** is a platform designed to predict and alert citizens of Kerala about the risk of waterborne disease outbreaks (Cholera, Typhoid, Hepatitis, etc.) based on real-time environmental data and historical trends.

## 2. Technology Stack & Tools Used

### **Backend (The Core Engine)**
- **Python 3.x**: Primary programming language for logic and data processing.
- **Flask**: Lightweight web framework used to build the RESTful API and Admin Dashboard.
- **Gunicorn**: Production-grade WSGI HTTP Server used for stable deployment on Render.
- **Scikit-Learn**: Used for building and executing the Machine Learning model (Random Forest).
- **Pandas**: Used for data manipulation, merging, and preprocessing of the DHS datasets.
- **Joblib**: Used for efficient serialization and loading of the trained [.pkl](file:///d:/waterborne-disease-ai/model/disease_risk_model.pkl) model.

### **Frontend & Mobile (User Interface)**
- **HTML5 & Vanilla CSS3**: Structured with a "Premium Glassmorphism" aesthetic and dynamic micro-animations.
- **Vanilla JavaScript**: Handles geolocation, API calls, and UI state management without heavy framework overhead.
- **Chart.js**: Utilized in the Admin Dashboard for visualizing historical risk trends and district data.
- **PWA (Progressive Web App)**: Configured with a [manifest.json](file:///d:/waterborne-disease-ai/twa-manifest.json) and a custom Service Worker (`sw.js`) for offline caching and home-screen installation.
- **TWA (Trusted Web Activity)**: The PWA is wrapped into a native Android [.apk](file:///d:/waterborne-disease-ai/app-release-signed.apk)/[.aab](file:///d:/waterborne-disease-ai/app-release-bundle.aab) using Google's **Bubblewrap** and **Node.js**.

### **APIs & Services**
- **OpenWeatherMap API**: Fetches real-time rainfall, temperature, and humidity data for any city or coordinate.
- **IPAPI**: Used as a high-reliability fallback for geolocation when hardware GPS is unavailable or timed out.
- **PyWebPush**: Implements the VAPID (Voluntary Application Server Identification) protocol to send encrypted push notifications.
- **Render**: The cloud hosting platform used for the live deployment of the Python backend.

---

## 3. Data Methodology: Merging & Training

### **The Datasets**
The system logic is built on two primary data streams:
1.  **Historical Health Data**: Authentic case counts from the **Kerala Directorate of Health Services (DHS) IDSP** reports (2013–2023).
2.  **Environmental Data**: Weather averages for Kerala districts (Rainfall, Humidity, Temperature) mapped to the health reports.

### **Merging & Preprocessing**
- **Data Alignment**: Health case counts were manually mapped to the corresponding year and district's meteorological profile.
- **Cleaning**: Outliers were handled using Pandas, and missing values in weather reports were filled using regional averages.
- **Normalization**: District names were normalized (e.g., "Kochi" maps to "Ernakulam") using a fuzzy-matching utility ([utils/risk_explain.py](file:///d:/waterborne-disease-ai/utils/risk_explain.py)) to ensure consistency across APIs.

### **Model Training (Machine Learning)**
- **Algorithm**: **Random Forest Classifier**. Selected for its robustness against small datasets and its ability to handle non-linear relationships between rainfall and disease.
- **Training Process**: The model was trained on the [merged_real_data.csv](file:///d:/waterborne-disease-ai/data/merged_real_data.csv) dataset. Since the sample size is relatively small (district-wise annual snapshots), **Cross-Validation** was used instead of a standard train/test split to ensure maximum accuracy.
- **Feature Importance**: The model identifies `rainfall_mm` and `flood` history as the most significant predictors of waterborne disease risk.

---

## 4. Data Sources & Collection

The 2013-2023 historical data was meticulously collected and cross-referenced from the following official authorities:

1.  **Kerala Directorate of Health Services (DHS)**: Specialized case counts for waterborne diseases (Cholera, Typhoid, Hepatitis, and Leptospirosis) were extracted from the **Integrated Disease Surveillance Programme (IDSP)** annual archives.
2.  **India Meteorological Department (IMD)**: Historical meteorological metrics including district-wise annual rainfall (mm), humidity index (%), and average temperatures (°C) were sourced from **IMD Pune** and **Regional Meteorological Centre (Thiruvananthapuram)** datasets.
3.  **National Disaster Management Authority (NDMA)**: Verified flood occurrence data for the state of Kerala (specifically for the 2018 and 2021 extreme events) was used to train the flood-risk impact feature.

---

## 5. Comprehensive Dataset Reference

The project utilizes several datasets stored in the [data/](file:///d:/waterborne-disease-ai/app/app.py#207-220) directory to power the training and live features:

| Dataset File | Type | Description |
| :--- | :--- | :---|
| [merged_real_data.csv](file:///d:/waterborne-disease-ai/data/merged_real_data.csv) | **Primary Training** | Final processed dataset containing 2013-2023 district-wise weather and health metrics. |
| [disease_cases_real.csv](file:///d:/waterborne-disease-ai/data/disease_cases_real.csv)| **Historical Health** | Authentic waterborne disease case counts from the Kerala DHS IDSP 2022 reports. |
| [raw_weather_data_real.csv](file:///d:/waterborne-disease-ai/data/raw_weather_data_real.csv)| **Meteorological** | 10-year historical weather data (Rainfall, Humidity, Temp) for all 14 Kerala districts. |
| [disease_cases.csv](file:///d:/waterborne-disease-ai/data/disease_cases.csv) | **Prototyping** | Baseline health dataset used for initial architecture validation. |
| [raw_weather_data.csv](file:///d:/waterborne-disease-ai/data/raw_weather_data.csv) | **Prototyping** | Initial weather mapping used during the early development phase. |
| [subscriptions.json](file:///d:/waterborne-disease-ai/data/subscriptions.json) | **Dynamic Data** | Encrypted JSON storage for user push notification endpoints. |
| [vapid.json](file:///d:/waterborne-disease-ai/data/vapid.json) | **Security** | Contains the Public and Private VAPID keys for secure notification authentication. |

---

## 5. Risk Assessment Logic

### **On What Basis is Risk Shown?**
The system calculates risk by ingesting **four real-time inputs**:
1.  **Rainfall (mm)**: High rainfall leads to water contamination and runoff.
2.  **Temperature (°C)**: Specific temperatures accelerate the growth of bacteria like *Vibrio cholerae*.
3.  **Humidity (%)**: High humidity correlates with monsoon conditions and vector breeding.
4.  **Flood History**: Binary indicator (Yes/No) of recent flooding in the area.

### **Risk Calculation Scale**
Risk is categorized into three data-driven tertiles:
-   **LOW (Level 0)**: < 20,000 annual cases in historical data. Environment is stable.
-   **MEDIUM (Level 1)**: 20,000 – 46,000 annual cases. High rainfall or humidity detected.
-   **HIGH (Level 2)**: > 46,000 annual cases. Extreme monsoon conditions or active flooding.

### **Predictive Heuristics**
Beyond the ML model, the system uses a **Heuristic Layer** to prevent false positives. For example, if the machine learning model predicts a risk based on temperature but the rainfall is 0mm (dry season), the system may downgrade the risk to "Low" to ensure alerts remain meaningful and accurate for the user.

---

## 5. Minute Implementation Details

### **Dual-Layer Geolocation**
To ensure the "Zero-Click" experience works every time:
1.  The app first attempts an **HTML5 High-Accuracy GPS** request.
2.  If the request fails (e.g., indoor usage) or times out (after 5 seconds), it silently switches to **IP Geolocation** via `ipapi`.
3.  This ensures the user sees their district's risk immediately upon opening the app.

### **Native Android Integration**
- **Digital Asset Links**: `assetlinks.json` facilitates a "Trusted" relationship between the website and the Android OS, allowing the app to bypass the "Chrome" url bar and act like a native application.
- **Service Worker Lifecycle**: The `sw.js` handles background push synchronization, allowing Health Authorities to send alerts even when the user's app is closed.
- **VAPID Security**: Push notifications are signed with a private VAPID key pair, ensuring that only the official dashboard can send alerts to the subscribers' devices.
