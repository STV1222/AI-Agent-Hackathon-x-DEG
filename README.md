# Grid-Scale Demand Flexibility Agent

An AI-powered agentic orchestration system for Distribution System Operators (DSOs) that forecasts grid overloads, discovers Distributed Energy Resources (DERs) via Beckn Protocol, and coordinates load flexibility to prevent feeder-level congestion and outages.

## 🎬 Demo Video

[![Demo Video](https://img.youtube.com/vi/jDOHLDDqOqw/maxresdefault.jpg)](https://www.youtube.com/watch?v=jDOHLDDqOqw)

**Watch the full demo** showing our AI-powered agent forecasting grid risks and orchestrating DERs through Beckn Protocol.

---

## 🎯 Problem Focus

**Problem Statement 1: Utility Interface with Agentic Orchestration for Grid-Scale Demand Flexibility**

As distributed energy resources (DERs) proliferate behind-the-meter, utilities struggle to autonomously monitor and mitigate feeder-level spikes in real-time. Manual coordination is slow, expensive, and lacks visibility and traceability.

**Our Solution:** An autonomous agent that acts as a reliable co-pilot for DSOs (e.g., UK Power Networks) to forecast and manage local load flexibility at feeder/substation levels, aligned with Ofgem's flexibility reforms.

### Key Capabilities

- ✅ **Beckn Protocol Integration**: Discovers available catalogues of subscribed DERs and orchestrates activation
- ✅ **AI-Powered Flexibility Planning**: Uses Google Gemini to generate optimized DER dispatch plans
- ✅ **Grid Risk Assessment**: Forecasts localized grid overloads using weather and load data
- ✅ **DER Coordination**: Coordinates load shifting/shedding (battery discharge, EV deferment, HVAC shifting)
- ✅ **Command-Centre Dashboard**: Real-time visualization of grid assets, risks, and DER orchestration
- ✅ **Audit Logging**: Timestamped decisions, data sources, and DER responses

---

## 🏗️ Solution Overview

The system operates as a **three-stage workflow**:

1. **Simulation & Risk Assessment**: Analyze weather scenarios and forecast grid congestion risks at feeder/substation levels
2. **AI Flexibility Planning**: Generate optimized DER dispatch plans using AI agent
3. **Beckn Orchestration**: Discover and activate DERs through Beckn Protocol workflows (Search → Select → Confirm)

### DER Types Supported

- **Battery Discharge**: Virtual Power Plant (VPP) and commercial battery storage
- **EV Load Reduction**: Smart charging curtailment via ChargePoint Network
- **HVAC Load Shifting**: Commercial HVAC pre-cooling and load shifting
- **Mobile Generation**: Emergency backup power deployment

---

## 🛠️ Technical Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  Scenario    │  │ Risk & AI    │  │   Beckn      │   │
│  │   Panel      │  │   Panel      │  │    Log       │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│  ┌────────────────────────────────────────────────────┐   │
│  │           Map View (Leaflet)                       │   │
│  └────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP/REST
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Backend (FastAPI)                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   Risk       │  │     AI       │  │    Beckn      │   │
│  │  Engine      │  │   Agent     │  │   Service     │   │
│  │              │  │  (Gemini)   │  │  (BAP/BPP)    │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                             │
│  ┌────────────────────────────────────────────────────┐   │
│  │         Mock BPP (DER Catalog Provider)             │   │
│  └────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Beckn Protocol
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              DER Providers (Mocked)                         │
│  • Tesla Virtual Power Plant                                │
│  • ChargePoint Network                                       │
│  • Honeywell Smart Grid Solutions                           │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Backend:**
- **Python 3.12+** with FastAPI
- **Google Gemini API** for AI agent
- **Pydantic** for data validation
- **httpx** for async HTTP (Beckn Protocol)
- **uv** for dependency management

**Frontend:**
- **React** with modern hooks
- **Leaflet** for interactive maps
- **CSS3** with dark theme

**Protocol:**
- **Beckn Protocol** (v0.9.3) for DER discovery and orchestration
- **BAP (Buyer App Protocol)** client implementation
- **BPP (Buyer Provider Protocol)** mock server

### Data Flow

1. **Scenario Input** → Weather event (heatwave/flood) triggers risk assessment
2. **Risk Engine** → Calculates grid congestion risks based on load projections
3. **AI Agent** → Analyzes risks and generates DER dispatch plan
4. **Beckn Service** → Discovers DERs via Search, selects optimal provider, confirms order
5. **Audit Logging** → Records all decisions and DER responses

---

## 🔄 Agent Workflow

### Stage 1: Simulation & Risk Assessment

```
User Input (Scenario)
    │
    ├─ Location: "London"
    ├─ Event Type: "heatwave" | "flood"
    ├─ Start Date: ISO timestamp
    └─ Duration: hours
    │
    ▼
POST /scenario/run
    │
    ├─ Load Assets (substations, EV hubs, solar farms)
    ├─ Get Weather Data (mock weather service)
    └─ Calculate Risks (risk_engine.py)
    │
    ▼
Risk Results
    ├─ CRITICAL: Load > 120% capacity
    ├─ HIGH: Load > 105% capacity
    ├─ MEDIUM: Load approaching 95% capacity
    └─ LOW: Monitor reserve margins
```

### Stage 2: AI Flexibility Planning

```
Risk Assessment Results
    │
    ▼
POST /agent/mitigate
    │
    ├─ Scenario Context
    ├─ Identified Risks (Grid Constraints)
    └─ Asset Inventory
    │
    ▼
AI Agent (Google Gemini)
    │
    ├─ Prompt: "DSO Flexibility Orchestrator"
    ├─ Task: Generate Flexibility Dispatch Plan
    └─ Prioritize: Non-wires alternatives (DERs)
    │
    ▼
Mitigation Actions
    ├─ asset_id: Feeder/substation requiring relief
    ├─ action_type: DER service type
    │   ├─ dispatch_battery_discharge
    │   ├─ reduce_ev_load
    │   ├─ shift_hvac_load
    │   └─ deploy_mobile_generator
    ├─ urgency: low | medium | high
    ├─ justification: Technical reason
    └─ target_time: ISO timestamp
```

### Stage 3: Beckn Orchestration

```
Mitigation Actions
    │
    ▼
POST /beckn/execute
    │
    ▼
For each action:
    │
    ├─┐
    │ │ Beckn Search
    │ ├─ POST /mock-bpp/search
    │ ├─ Query: action_type (e.g., "dispatch_battery_discharge")
    │ └─ Wait for on_search callback
    │   │
    │   ▼
    │   Catalog Response
    │   ├─ Provider: "Tesla Virtual Power Plant"
    │   └─ Items: Available DER services
    │
    ├─┐
    │ │ Beckn Select
    │ ├─ POST /mock-bpp/select
    │ ├─ Select: Best DER service
    │ └─ Wait for on_select callback
    │   │
    │   ▼
    │   Quote Response
    │   ├─ Price: GBP per kWh
    │   └─ Terms: Service details
    │
    └─┐
      │ Beckn Confirm
      ├─ POST /mock-bpp/confirm
      ├─ Confirm: Order DER service
      └─ Wait for on_confirm callback
        │
        ▼
      Order Confirmed
      ├─ Order ID: ORD-xxxxx
      ├─ Status: "Created"
      └─ Provider: DER activated
```

### Complete Flow Diagram

```
┌─────────────┐
│   User      │
│  Dashboard  │
└──────┬──────┘
       │
       │ 1. Run Scenario
       ▼
┌─────────────────┐      ┌──────────────┐      ┌─────────────┐
│  Risk Engine    │─────▶│  Weather     │─────▶│   Assets   │
│                 │      │   Service    │      │   (DEG)    │
└────────┬────────┘      └──────────────┘      └─────────────┘
         │
         │ 2. Risk Results
         ▼
┌─────────────────┐
│   AI Agent      │
│   (Gemini)      │
└────────┬────────┘
         │
         │ 3. Flexibility Plan
         ▼
┌─────────────────┐
│  Beckn Service  │
│   (BAP Client)  │
└────────┬────────┘
         │
         │ 4. Search → Select → Confirm
         ▼
┌─────────────────┐      ┌──────────────┐
│   Mock BPP      │◀─────│  DER Catalog │
│   (Server)      │      │   Providers  │
└────────┬────────┘      └──────────────┘
         │
         │ 5. Order Confirmed
         ▼
┌─────────────────┐
│  Audit Log      │
│  (Transaction)  │
└─────────────────┘
```

---

## 🚀 Setup Instructions

### Prerequisites

- **Python 3.12+** ([Download](https://www.python.org/downloads/))
- **Node.js 16+** and npm ([Download](https://nodejs.org/))
- **Google Gemini API Key** ([Get it here](https://makersuite.google.com/app/apikey))
- **uv** (Python package manager) - Optional but recommended

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   
   **Option A: Using uv (Recommended)**
   ```bash
   uv sync
   ```
   
   **Option B: Using venv + pip**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install fastapi uvicorn pydantic python-dotenv google-generativeai httpx
   ```

3. **Create `.env` file:**
   ```bash
   echo "GOOGLE_API_KEY=your_api_key_here" > .env
   ```
   
   Or manually create `backend/.env`:
   ```
   GOOGLE_API_KEY=your_actual_google_api_key
   ```

4. **Run the server:**
   ```bash
   # Using uv
   uv run uvicorn main:app --reload
   
   # Using venv
   uvicorn main:app --reload
   ```

   The backend API will be available at: **http://localhost:8000**

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

   The frontend will be available at: **http://localhost:3000**

### Verify Installation

1. **Backend Health Check:**
   ```bash
   curl http://localhost:8000/
   ```
   Should return API status and available endpoints.

2. **Frontend:** Open http://localhost:3000 in your browser.

---

## 📡 API Endpoints

### Scenario & Risk Assessment

**POST `/scenario/run`**
- Run risk simulation for a weather scenario
- **Request:**
  ```json
  {
    "location": "London",
    "event_type": "heatwave",
    "start_date": "2025-11-26T00:00:00Z",
    "duration_hours": 72
  }
  ```
- **Response:** Scenario, assets, and risk results

### AI Agent

**POST `/agent/mitigate`**
- Generate AI-powered flexibility dispatch plan
- **Request:** Scenario, risks, and assets
- **Response:** Summary text and mitigation actions

### Beckn Orchestration

**POST `/beckn/execute`**
- Execute Beckn Protocol workflow for DER activation
- **Request:** List of mitigation actions
- **Response:** Transaction log with provider confirmations

### Beckn Callbacks (BAP)

- **POST `/beckn/on_search`** - Receive DER catalog from BPP
- **POST `/beckn/on_select`** - Receive quote from BPP
- **POST `/beckn/on_confirm`** - Receive order confirmation from BPP

### Mock BPP Endpoints

- **POST `/mock-bpp/search`** - Search DER catalog
- **POST `/mock-bpp/select`** - Select DER service
- **POST `/mock-bpp/confirm`** - Confirm DER order

---

## 📁 Project Structure

```
.
├── backend/                 # Python FastAPI backend
│   ├── main.py             # FastAPI app & API endpoints
│   ├── agent_service.py    # AI agent (Google Gemini)
│   ├── risk_engine.py      # Grid risk calculation
│   ├── beckn_service.py   # Beckn orchestration logic
│   ├── beckn_bap.py       # BAP client implementation
│   ├── beckn_models.py    # Beckn Protocol models
│   ├── mock_bpp.py        # Mock BPP server
│   ├── weather.py         # Weather data service
│   ├── utils.py           # Utility functions
│   ├── pyproject.toml     # Python dependencies
│   └── .env               # Environment variables (create this)
│
├── frontend/               # React frontend
│   ├── src/
│   │   ├── App.js         # Main app component
│   │   ├── App.css        # App styles
│   │   ├── components/    # React components
│   │   │   ├── ScenarioPanel.js
│   │   │   ├── RiskPanel.js
│   │   │   ├── BecknLog.js
│   │   │   ├── MapView.js
│   │   │   └── LoadingSpinner.js
│   │   └── index.js       # Entry point
│   └── package.json       # Node dependencies
│
├── data/                  # Mock data files
│   ├── assets.json        # DEG assets (substations, EV hubs, etc.)
│   └── scenarios.json     # Predefined scenarios
│
├── documents/             # Documentation
│   ├── problem_statement.md
│   └── Design Document Design.pdf
│
└── README.md              # This file
```

---

## 🔍 Key Features

### 1. Real-Time Risk Assessment
- Forecasts grid congestion based on weather patterns
- Calculates load projections at feeder/substation levels
- Identifies CRITICAL, HIGH, MEDIUM, and LOW risk scenarios

### 2. AI-Powered DER Planning
- Uses Google Gemini to analyze grid constraints
- Generates optimized flexibility dispatch plans
- Prioritizes non-wires alternatives (DERs) over physical interventions

### 3. Beckn Protocol Integration
- Full implementation of Beckn workflows
- Discovers DERs from subscribed catalogues
- Orchestrates Search → Select → Confirm flow

### 4. Command-Centre Dashboard
- Step-by-step wizard interface
- Real-time map visualization (Leaflet)
- Risk assessment and DER coordination panels
- Beckn transaction logs

### 5. Mock DER Providers
- Tesla Virtual Power Plant (battery discharge)
- ChargePoint Network (EV load reduction)
- Honeywell Smart Grid Solutions (HVAC shifting)

---

## 🧪 Testing the System

1. **Start Backend:**
   ```bash
   cd backend
   uv run uvicorn main:app --reload
   ```

2. **Start Frontend:**
   ```bash
   cd frontend
   npm start
   ```

3. **Run a Scenario:**
   - Open http://localhost:3000
   - Select location: "London"
   - Choose event type: "heatwave"
   - Set duration: 72 hours
   - Click "Run Simulation"

4. **Get AI Mitigation Plan:**
   - Review risk assessment results
   - Click "Get AI Mitigation Plan"
   - Review DER dispatch recommendations

5. **Execute via Beckn:**
   - Click "Execute via Beckn Network"
   - Watch Beckn transaction logs
   - See DER provider confirmations

---

## 🔐 Environment Variables

Create `backend/.env`:
```
GOOGLE_API_KEY=your_google_gemini_api_key
```

---

## 📚 Additional Documentation

- **Problem Statement:** See `documents/problem_statement.md`
- **Setup Guide:** See `SETUP.md` (if available)
- **API Contracts:** See `docs/API_CONTRACTS.md` (if available)

---

## 🛣️ Roadmap & Future Enhancements

### Minimum Requirements (In Progress)
- [x] Beckn Protocol implementation
- [x] AI agent integration
- [x] Risk assessment engine
- [x] DER discovery via Beckn
- [ ] Real-time feeder monitoring (<5s SLA)
- [ ] P415 VLP activation & OBP IDs
- [ ] Enhanced audit logs (data sources, operator rules)
- [ ] Grid load forecasting (historical + real-time)

### Good-to-Have Features
- [ ] Self-analysis for exceptional scenarios
- [ ] Multi-feeder failure handling
- [ ] Incentive vs. emergency intervention differentiation
- [ ] Carbon intensity tracking
- [ ] Cost optimization algorithms

---

## 👥 Team

- **Backend & Data Lead**: Backend API, Beckn Protocol, Risk Engine
- **AI & Frontend Lead**: AI Agent, Frontend Dashboard, UI/UX

---

## 📄 License

This project is developed for the AI Agent Hackathon x DEG.

---

## 🤝 Contributing

This is a hackathon project. For questions or contributions, please contact the team.

---

**Built with ❤️ for Grid-Scale Demand Flexibility**
