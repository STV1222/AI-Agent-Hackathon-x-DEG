# Extreme Weather Resilience Agent

An AI agent that uses weather + energy network data on the **Digital Energy Grid (DEG)** to simulate how heatwaves/floods impact local energy infrastructure, then **recommends and orchestrates mitigation actions via Beckn-style open network services**.

## Project Structure

```
.
├── backend/           # Python + FastAPI backend
├── frontend/          # React frontend (or Streamlit alternative)
├── data/             # Mock data files (DEG assets, weather scenarios)
├── docs/             # Documentation and planning
└── README.md
```

## Tech Stack

- **Backend**: Python 3.10+, FastAPI
- **AI Agent**: LLM API (OpenAI/Claude)
- **Frontend**: React + Leaflet (or Streamlit as alternative)
- **Data**: Mock DEG assets, weather APIs (Open-Meteo/OpenWeather)

## Setup

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Setup (React)

```bash
cd frontend
npm install
npm start
```

### Frontend Setup (Streamlit Alternative)

```bash
cd frontend/streamlit
pip install -r requirements.txt
streamlit run app.py
```

## Day 1 Goals

✅ Repo + skeleton backend & frontend  
✅ Asset mock data ready  
✅ Clear JSON contracts between backend ↔ AI ↔ frontend

## API Endpoints (Planned)

- `POST /scenario/run` - Run risk simulation for a scenario
- `POST /agent/mitigate` - Call AI agent and return mitigation actions
- `POST /beckn/execute` - Simulate Beckn search/confirm for actions

## Team

- **Teammate A**: Backend & Data Lead
- **Teammate B**: AI & Frontend Lead

