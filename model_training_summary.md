# Machine Learning Model & Data Merging Summary

This document explains the technical methodology used to prepare the datasets and train the predictive model for the AI Waterborne Disease Early Warning System.

## 1. Data Merging Process

The final training dataset (`merged_real_data.csv`) was created by synthesizing two primary streams of information:

### **A. Health Data Extraction**
- **Source**: Kerala Directorate of Health Services (DHS) Integrated Disease Surveillance Programme (IDSP) reports (2013–2023).
- **Method**: Data was extracted from official PDF archives using a custom PDF parsing script ([extract_dhs_pdf.py](file:///d:/waterborne-disease-ai/utils/extract_dhs_pdf.py)).
- **Metrics**: Annual case counts for Cholera, Typhoid, Hepatitis, and Leptospirosis were aggregated per district.

### **B. Environmental Data Compilation**
- **Source**: India Meteorological Department (IMD) historical records.
- **Method**: 10 years of district-wise meteorological data was compiled, including:
  - **Rainfall (mm)**: Annual totals and monsoon intensity.
  - **Temperature (°C)**: Annual averages.
  - **Humidity (%)**: Average moisture levels.
  - **Flood History**: Binary indicators (0/1) for districts affected by major floods (e.g., 2018, 2019, 2021).

### **C. The "District-Year" Join**
The [build_real_dataset.py](file:///d:/waterborne-disease-ai/utils/build_real_dataset.py) script performed a relational join on the **Year** and **District** keys, ensuring each row contained both the environmental conditions and the resulting health outcomes for that specific period and location.

---

## 2. Model Training Methodology

The predictive engine uses a supervised learning approach to categorize disease risk.

### **Algorithm: Random Forest Classifier**
- **Why?**: Selected for its ability to handle non-linear relationships and its robustness against the "noise" typical in environmental health data.
- **Features**: The model weights `rainfall_mm` and `flood` history most heavily, as these show the strongest correlation with waterborne outbreaks.

### **Training Workflow**
1. **Data Labeling**: Annual case counts were categorized into three data-driven risk levels (Low, Medium, High).
2. **Feature Engineering**: Normalized district averages and flood indicators were fed into the model.
3. **Validation**: Used **Cross-Validation** (via `scikit-learn`) rather than a simple train/test split. This is critical for smaller historical datasets to ensure the model generalizes well across different years.
4. **Serialization**: The final model was serialized using `joblib` into [disease_risk_model.pkl](file:///d:/waterborne-disease-ai/model/disease_risk_model.pkl) for high-speed inference in the production Flask app.

---

## Technical File Reference
- **Merging Script**: [utils/build_real_dataset.py](file:///d:/waterborne-disease-ai/utils/build_real_dataset.py)
- **Training Script**: [model/train_model_real.py](file:///d:/waterborne-disease-ai/model/train_model_real.py)
- **Final Dataset**: [data/merged_real_data.csv](file:///d:/waterborne-disease-ai/data/merged_real_data.csv)
- **Saved Model**: [model/disease_risk_model.pkl](file:///d:/waterborne-disease-ai/model/disease_risk_model.pkl)
