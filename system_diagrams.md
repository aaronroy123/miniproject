# Waterborne Disease AI - System Diagrams

## 1. System Architecture Diagram

This diagram visualizes the multi-layered, decoupled architecture defined in Chapter 3, representing the data flow from the Progressive Web App (PWA) client to the generative AI protocols.

```mermaid
graph TD
    classDef frontend fill:#3b82f6,stroke:#1e3a8a,stroke-width:2px,color:#fff,rx:5,ry:5;
    classDef routing fill:#10b981,stroke:#047857,stroke-width:2px,color:#fff,rx:5,ry:5;
    classDef standardization fill:#f59e0b,stroke:#b45309,stroke-width:2px,color:#fff,rx:5,ry:5;
    classDef datastore fill:#8b5cf6,stroke:#5b21b6,stroke-width:2px,color:#fff,rx:5,ry:5;
    classDef mathLogic fill:#ef4444,stroke:#b91c1c,stroke-width:2px,color:#fff,rx:5,ry:5;
    classDef generative fill:#ec4899,stroke:#be185d,stroke-width:2px,color:#fff,rx:5,ry:5;
    classDef external fill:#475569,stroke:#1e293b,stroke-width:2px,color:#fff,stroke-dasharray: 5 5,rx:5,ry:5;

    subgraph Client ["Client Device (Mobile / Browser View)"]
        UI["Presentation Layer (PWA UI)"]:::frontend
        Geo["HTML5 Geolocation / Telemetry"]:::frontend
        SW["Service Worker (Caching & Alerts)"]:::frontend
    end

    subgraph Engine ["Serverless Cloud Backend (Render / Flask / Gunicorn)"]
        Router["Application Routing & Web Hook Layer"]:::routing
        Standardize["Data Standardization & Phonetic Syncing"]:::standardization
        
        subgraph Databases ["Benchmarking Modules (Pandas)"]
            DHS["10-Year Kerala DHS Matrices"]:::datastore
            WHO["Global WHO Safety Heuristics"]:::datastore
        end
        
        Algo["Algorithmic Target Evaluation (e.g., > 35°C Trigger)"]:::mathLogic
        Cache["In-Memory State Dictionary / Cache"]:::routing
    end

    subgraph ExternalServices ["External Third-Party Integrations"]
        WeatherAPI["OpenWeather API (Live Hydrometeorology)"]:::external
        Gemini["Google Gemini API (LLM)"]:::external
    end

    %% Data flow mapping
    UI -->|Coordinates| Geo
    Geo -.->|Asynchronous XHR| Router
    Router --> Standardize
    Router <--> Cache
    
    Standardize -->|Retrieve Live Environment| WeatherAPI
    WeatherAPI -->|JSON Rainfall/Temp Data| Standardize
    
    Router -->|Pass Normalized Location| Databases
    
    Standardize --> Algo
    Databases -->|Historical Baselines| Algo
    
    Algo -->|Outbreak Risk Scores| Gemini
    Gemini -->|Actionable Diagnostic Protocol| Router
    
    Router -->|Updates Context Variables| UI
    Router -->|Pushes Threat Criticality| SW
```

<br>

## 2. System Use Case Diagram

This diagram maps the interaction layers between the primary system actors (Human vs AI APIs) and the core functional capabilities described in the software engineering methodology.

```mermaid
graph LR
    %% Defining Actors
    User("👤 Public Health Provider / General User"):::actorNode
    Weather("☁️ OpenWeather API"):::extNode
    Gemini("🤖 Google Generative AI"):::extNode

    %% Defining Use Cases
    UC1(["[UC1] Passively Transmit Telemetry / Location"]):::ucNode
    UC2(["[UC2] Monitor Live Risk & Weather Widget"]):::ucNode
    UC3(["[UC3] Execute Cross-Decade DHS Benchmarking"]):::ucNode
    UC4(["[UC4] Generate AI Clinical Disease Protocol"]):::ucNode
    UC5(["[UC5] Receive Autonomic Mobile Push Notifications"]):::ucNode

    %% Connecting User to use cases
    User --- UC1
    User --- UC2
    User --- UC3
    User --- UC4
    User --- UC5

    %% Dependencies and External Integrations
    UC1 -.->|Requires Live Data From| Weather
    UC2 -.->|Visualizes Data From| Weather
    UC4 -.->|Infers Intelligence Via| Gemini

    %% Apply visual styling
    classDef actorNode fill:#f8fafc,stroke:#94a3b8,stroke-width:2px,color:#1e293b,font-weight:bold;
    classDef extNode fill:#f1f5f9,stroke:#64748b,stroke-width:2px,color:#0f172a,stroke-dasharray: 4 4;
    classDef ucNode fill:#e0f2fe,stroke:#0ea5e9,stroke-width:2px,color:#0369a1,rx:20,ry:20;
```
