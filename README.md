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

## Quick Setup

**📖 For detailed setup instructions, see [SETUP.md](./SETUP.md)**

### Prerequisites
- Python 3.12+
- Node.js 16+ and npm
- Google Gemini API Key ([Get it here](https://makersuite.google.com/app/apikey))

### Backend Setup

```bash
cd backend

# Install dependencies (using uv - recommended)
uv sync

# OR using venv + pip
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install fastapi uvicorn pydantic python-dotenv google-generativeai httpx

# Create .env file with your API key
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# Run the server
uv run uvicorn main:app --reload
# OR: uvicorn main:app --reload (if using venv)
```

**⚠️ Important:** Create a `.env` file in the `backend/` directory with:
```
GOOGLE_API_KEY=your_actual_google_api_key
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

The app will be available at:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000

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
