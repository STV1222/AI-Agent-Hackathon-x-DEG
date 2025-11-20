# Project Structure

```
AI_AGENT_HACKATHON/
│
├── README.md                    # Main project documentation
├── .gitignore                   # Git ignore file
│
├── backend/                     # Python + FastAPI Backend
│   ├── main.py                 # Main FastAPI app with all endpoints
│   ├── utils.py                # Utility functions (data loading)
│   ├── requirements.txt        # Python dependencies
│   └── .env.example            # Environment variables template
│
├── frontend/                    # React Frontend
│   ├── package.json            # Node.js dependencies
│   ├── public/
│   │   └── index.html          # HTML template
│   └── src/
│       ├── index.js            # React entry point
│       ├── index.css           # Global styles
│       ├── App.js              # Main App component
│       ├── App.css             # App styles
│       └── components/
│           ├── ScenarioPanel.js      # Scenario configuration panel
│           ├── ScenarioPanel.css
│           ├── MapView.js            # Map with assets visualization
│           ├── MapView.css
│           ├── RiskPanel.js          # Risk assessment & AI output panel
│           ├── RiskPanel.css
│           ├── BecknLog.js           # Beckn network activity log
│           └── BecknLog.css
│
├── data/                        # Mock Data Files
│   ├── assets.json             # 20+ London DEG assets (substations, EV hubs, solar)
│   └── scenarios.json          # 3 predefined scenarios (heatwave, flood)
│
└── docs/                        # Documentation
    ├── API_CONTRACTS.md        # JSON schemas & API contracts
    ├── DAY1_CHECKLIST.md       # Day 1 tasks checklist
    ├── QUICK_START.md          # Setup instructions
    ├── NEXT_STEPS.md           # What to do now (Day 1 guide)
    └── PROJECT_STRUCTURE.md    # This file
```

## Component Overview

### Backend (`backend/`)

**main.py**: 
- FastAPI application
- Three main endpoints:
  - `POST /scenario/run` - Run risk simulation
  - `POST /agent/mitigate` - Get AI mitigation plan
  - `POST /beckn/execute` - Execute Beckn services
- Pydantic models for all JSON contracts
- CORS middleware for frontend connection

**utils.py**:
- `load_assets()` - Load DEG assets from JSON
- `load_scenarios()` - Load predefined scenarios
- `get_scenario_by_id()` - Get specific scenario

### Frontend (`frontend/`)

**App.js**:
- Main application component
- Manages state (scenario, assets, risks, mitigation plan)
- API calls to backend
- Layout: Left panel (scenario) + Center (map) + Right (risks) + Bottom (Beckn log)

**Components**:
- `ScenarioPanel`: Input scenario parameters, quick scenarios
- `MapView`: Leaflet map showing assets colored by risk level
- `RiskPanel`: Display risks, AI mitigation plan, action buttons
- `BecknLog`: Show Beckn network activity log

### Data (`data/`)

**assets.json**:
- 20+ assets in London
- Types: substations, EV hubs, solar farms
- Fields: id, name, type, lat, lon, capacity_kw, criticality
- Some assets tagged with flood zones, hospital feeds, etc.

**scenarios.json**:
- `london_heatwave_3d`: 3-day heatwave scenario
- `london_flood_24h`: 24-hour flood scenario
- `london_heatwave_5d`: 5-day heatwave scenario

### Documentation (`docs/`)

- **API_CONTRACTS.md**: Complete JSON schemas for all entities
- **DAY1_CHECKLIST.md**: Tasks to complete on Day 1
- **QUICK_START.md**: Setup instructions for both teammates
- **NEXT_STEPS.md**: Detailed Day 1 guide with tasks

## Key Features Implemented

✅ Complete project structure  
✅ Backend skeleton with all endpoints defined  
✅ Frontend skeleton with all components created  
✅ Mock data (20+ assets, 3 scenarios)  
✅ JSON contracts defined (Pydantic models)  
✅ UI layout (scenario panel, map, risk panel, Beckn log)  
✅ Documentation for setup and development  

## What's Next (Day 1)

**Teammate A**: Set up backend environment, implement data loading in `/scenario/run`  
**Teammate B**: Set up frontend environment, test frontend-backend connection, draft LLM prompts  

See `docs/NEXT_STEPS.md` for detailed instructions.

