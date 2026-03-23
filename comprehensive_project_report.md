# Project Report: AI Waterborne Disease Early Warning System

## 1. Introduction
The state of Kerala, situated on the southwestern coast of India, is characterized by its unique geography, dense network of rivers, and intense monsoon seasons. While these features contribute to the state's natural beauty and agricultural productivity, they also make the region highly susceptible to waterborne diseases. Outbreaks of diseases such as Cholera, Typhoid, Hepatitis A, and Leptospirosis are frequent, particularly following extreme weather events like the devastating floods of 2018 and 2019.

Currently, the public health response in Kerala is largely reactive. Health authorities typically intervene after an outbreak has been identified through hospital case reports. This delay can lead to significant morbidity and mortality, as waterborne pathogens can spread rapidly through contaminated water sources. There is a critical need for a proactive, data-driven approach that can predict the risk of outbreaks before they occur.

This project introduces an **AI Waterborne Disease Early Warning System** designed specifically for the Kerala context. By leveraging machine learning and real-time meteorological data, the system provides localized risk assessments and instant alerts to citizens. The primary goal is to shift the paradigm from reactive crisis management to proactive prevention, empowering both health authorities and individual citizens with actionable intelligence.

---

## 2. Literature Review
To establish a foundation for this project, several key research areas were explored:

1.  **Groundwater Quality Prediction (2024)**: Recent studies in Kerala have utilized machine learning models like XGBoost and Random Forest to assess groundwater quality. High goodness-of-fit (R²: 0.922) for Random Forest models indicates that ML is highly effective at identifying regions where water quality is compromised, a primary precursor to waterborne disease outbreaks.
2.  **Climate-Sensitive Disease Forecasting**: Empirical analysis of climatic variability in Kerala has demonstrated that humidity and rainfall are the dominant factors influencing disease incidence. Research utilizing Random Forest and Gradient Boosting models has shown that meteorological features can accurately forecast outbreaks of climate-sensitive diseases.
3.  **Pathogen Survival and Climate Change**: Reports from the National Library of Medicine (NLM) highlight that climate change impacts waterborne diseases by altering pathogen replication and virulence. Heavy rainfall events in Kerala often compromise sanitation infrastructure, leading to rapid contamination—a relationship our model explicitly leverages via the "flood history" feature and critical temperature thresholds (set at **35°C**).
4.  **Machine Learning in Public Health**: Global research on waterborne disease prediction consistently demonstrates that algorithms like Random Forest are robust against the non-linear and noisy nature of environmental data, making them ideal for small, district-wise historical datasets.

---

## 3. System Development

### 3.1 Objectives
-   **Localized Prediction**: Provide district-specific risk levels for all 14 districts of Kerala.
*   **Real-time Intelligence**: Integrate live weather data (Rainfall, Humidity, Temperature) to update risk assessments instantly.
*   **Public Alerting**: Implement a high-reliability push notification system to broadcast emergency warnings.
*   **Accessibility**: Deploy as a cross-platform mobile application (PWA/TWA) that works even on low-bandwidth networks.

### 3.2 Proposed System
The proposed system is a multi-tier architecture consisting of a Python/Flask backend and an HTML5/JavaScript frontend. It utilizes a Random Forest Classifier to process live meteorological data against 10 years of historical Kerala Health Services (DHS) data. The system is designed for a "Zero-Click" user experience, using automated geolocation to present critical data immediately upon app launch.

### 3.3 Design and Methodologies
#### **Architecture (Multi-Layer)**
1.  **Presentation Layer**: A Progressive Web App (PWA) built with CSS Glassmorphism, providing a premium mobile interface.
2.  **Logic Layer**: A Flask-based API layer that orchestrates weather fetching, ML inference, and risk explanation.
3.  **Intelligence Layer**: The Scikit-Learn model (`disease_risk_model.pkl`) that categorizes risk into three tertiles.
4.  **Data Layer**: Persistent storage for user subscriptions and historical reference datasets.

#### **Methodology & Modules**
-   **Data Merging**: Historical case counts from DHS IDSP reports were merged with IMD weather records (2013-2023) using a relational "District-Year" join.
-   **ML Module**: A Random Forest Classifier with 100 estimators. Key features include `rainfall_mm`, `temperature`, `humidity`, and a binary `flood` indicator.
-   **Weather Module**: Connects to the OpenWeatherMap API to ingest live environmental parameters.
-   **Notification Module**: Utilizes the VAPID protocol and Service Workers to handle background push alerts.

---

## 4. Results and Discussion
The system was validated using historical data from the 2018 and 2019 Kerala floods. During these extreme events, the model correctly identified "High Risk" scenarios (Level 2) across the mostly affected central and northern districts.

**Model Performance**:
-   **Accuracy**: The model achieved high classification accuracy during cross-validation, effectively distinguishing between Low (<20k cases) and High (>46k cases) risk profiles.
-   **Heuristic Refinement**: To prevent false positives during the dry season, a heuristic layer was added. For instance, if the temperature is below **35°C** and there is no rainfall or flooding, the system automatically defaults the risk to "Low" to avoid thermal triggers in non-extreme heat.

---

## 5. Conclusion and Future Scope
The AI Waterborne Disease Early Warning System demonstrates that combining machine learning with real-time environmental APIs can provide a viable early detection mechanism for public health. By shifting from reactive to proactive monitoring, the platform can significantly reduce the impact of outbreaks in vulnerable regions like Kerala.

**Future Scope**:
-   **IoT Integration**: Incorporating live telemetry from water-quality sensors (pH, turbidity).
*   **Expansion**: Scaling the model to cover other states in the Western Ghats region.
*   **Multi-Channel Alerts**: Integrating WhatsApp and SMS gateways for users without smartphones.

---

## 6. References
1.  Kerala Directorate of Health Services (DHS), Integrated Disease Surveillance Programme (IDSP) Archives (2013-2023).
2.  India Meteorological Department (IMD) - Pune & Thiruvananthapuram Climate Records.
3.  "Groundwater Quality Prediction and Risk Assessment in Kerala using Machine Learning," *Public Health Journal*, 2024.
4.  "Climatic Variability and Disease Incidence: An Empirical Analysis of Kerala," *ResearchGate*, 2022.

---

## Appendix: Implementation Snapshots
-   **Backend Core**: [app/app.py](file:///d:/waterborne-disease-ai/app/app.py)
-   **ML Workflow**: [model/train_model_real.py](file:///d:/waterborne-disease-ai/model/train_model_real.py)
-   **Frontend UI**: [index.html](file:///d:/waterborne-disease-ai/app/templates/index.html)
-   **System Architecture**: [diagrams.md](file:///d:/waterborne-disease-ai/diagrams.md)
