# System Diagrams: Waterborne Disease AI

This document provides a technical overview of the system through Data Flow Diagrams (DFD) and UML models.

---

## 1. Data Flow Diagrams (DFD)

### Level 0: Context Diagram
The Context Diagram shows the system's boundaries and its interactions with external entities.

```mermaid
graph TD
    User((User / Citizen))
    Admin((Health Admin))
    API_SRV((Weather API))

    subgraph System [Waterborne Disease Early Warning System]
    end

    User -- "1. Input: City/District/Coords" --> System
    System -- "2. Output: Risk Alert & Precautions" --> User
    System -- "3. Request: Lat/Lon Weather" --> API_SRV
    API_SRV -- "4. Data: Rainfall, Temp, Humidity" --> System
    Admin -- "5. Login: Admin Access" --> System
    System -- "6. Report: District Analytics & Cases" --> Admin
    Admin -- "7. Broadcast: Emergency Notifications" --> System
    System -- "8. Alert: Push Notifications" --> User
```

### Level 1: Multi-Process Diagram
The Level 1 DFD breaks down the internal processes and data stores of the system.

```mermaid
graph TD
    %% Entities
    U[User / Citizen]
    A[Health Authority Admin]
    W[Weather API Server]

    %% Processes
    P1[1. Input & Weather Handler]
    P2[2. AI Risk Prediction Engine]
    P3[3. Risk Explainer & Report Gen]
    P4[4. Subscription & Push Manager]
    P5[5. Admin Dashboard Controller]

    %% Data Store
    D1[(Subscription Database - JSON)]

    %% Logic Flow
    U -- "Location Query" --> P1
    P1 -- "Request Data" --> W
    W -- "Meteorological Data" --> P1
    P1 -- "Cleaned Weather Features" --> P2
    P2 -- "Risk Score (0/1/2)" --> P3
    P3 -- "Safety Report & Context" --> U

    U -- "Store Subscription" --> P4
    P4 -- "Save Info" --> D1
    A -- "Manual Alert Trigger" --> P5
    P5 -- "Fetch Subscribers" --> D1
    D1 -- "Target Endpoints" --> P5
    P5 -- "Process Broadcast" --> P4
    P4 -- "Risk Notification" --> U

    A -- "Log in / Dashboard View" --> P5
    P5 -- "Request Real-time Prediction" --> P2
    P2 -- "District Data Analysis" --> P5
    P5 -- "Aggregated District View" --> A
```

---

## 2. UML Diagrams

### Use Case Diagram (Simplified Model)
```mermaid
graph LR
    Citizen -- Login --> UC1(Login System)
    Citizen -- Get Location --> UC2(Locate)
    Citizen -- View Risk --> UC3(Risk Level)
    Citizen -- Get Alerts --> UC4(Notification)
    
    Authority -- Monitor --> UC5(Dashboard)
    Authority -- Reports --> UC6(Analytics)
    Authority -- Send --> UC4
    Authority -- Manage --> UC7(Data Admin)

    UC2 -. include .-> FetchWeather
    UC5 -. include .-> FetchWeather
    FetchWeather -. include .-> UC3
    UC4 -. include .-> GenerateAlerts
    HighRisk -. extend .-> GenerateAlerts
```

### Sequence Diagram
```mermaid
sequenceDiagram
    User->>System: Get Risk Update
    System->>WeatherAPI: Fetch Regional Data
    WeatherAPI-->>System: Rainfall/Temp Response
    System->>System: Run ML Prediction
    System-->>User: Display Risk Alert
```

---

## 3. System Architecture
The overall architecture shows how components interact across different layers.

```mermaid
graph TB
    subgraph Presentation_Layer [Presentation Layer]
        PWA[Progressive Web App - HTML/JS/CSS]
        TWA[Android TWA Wrapper]
        SW[Service Workers - Caching & Push]
    end

    subgraph Application_Layer [Application Layer - Flask]
        Gunicorn[Gunicorn WSGI Server]
        API[Flask RESTful API]
        Auth[Admin Auth Module]
    end

    subgraph Logic_Layer [Intelligence & Utilities]
        Predictor[ML Predictor - Random Forest]
        Explainer[Risk Explanation Engine]
        WeatherSvc[Weather Integration Service]
    end

    subgraph Data_Layer [Data & Storage]
        JSON_DB[(Subscriptions.json - Persistence)]
        VAPID[(VAPID Keys - Push Auth)]
        Static[(GeoJSON & Assets)]
    end

    subgraph External_Services [External Cloud Services]
        OpenWeather[OpenWeatherMap API]
        Render[Render Hosting Platform]
        Push[Browser Push Service]
    end

    %% Interactions
    Presentation_Layer -- "HTTPS / JSON Requests" --> Application_Layer
    Application_Layer -- "Process Features" --> Logic_Layer
    Application_Layer -- "I/O Ops" --> Data_Layer
    Logic_Layer -- "Fetch Forecast" --> OpenWeather
    Application_Layer -- "Web Push Payload" --> Push
    Push -- "Direct Notification" --> Presentation_Layer
    Render -- "Hosts" --> Application_Layer
```
