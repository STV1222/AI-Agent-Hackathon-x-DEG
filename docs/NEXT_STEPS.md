# What to Do Now - Day 1 Guide

## ✅ What's Already Done

1. **Project Structure**: Complete directory structure created
2. **Backend Skeleton**: FastAPI app with all endpoints defined (empty implementations)
3. **Frontend Skeleton**: React app with all components created
4. **Mock Data**: 20+ London assets and 3 predefined scenarios
5. **JSON Contracts**: All schemas defined in `backend/main.py` and `docs/API_CONTRACTS.md`

## 🎯 Immediate Next Steps

### For Both Teammates

1. **Clone/Download this project** (if not already)
2. **Read through the structure**:
   - Check `README.md` for overview
   - Review `docs/API_CONTRACTS.md` for data formats
   - Look at `docs/DAY1_CHECKLIST.md` for tasks

### Teammate A - Backend & Data Lead

**Task 1: Set up Backend Environment** (15 min)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

**Task 2: Test Backend Runs** (5 min)
```bash
uvicorn main:app --reload
# Visit http://localhost:8000/docs to see API docs
# Visit http://localhost:8000 to see root endpoint
```

**Task 3: Implement Basic Data Loading** (30 min)
- Edit `backend/main.py`
- In `/scenario/run` endpoint:
  - Import `load_assets` from `utils.py`
  - Load assets based on location
  - Return mock assets (no risk calculation yet)
  - Test endpoint with Postman or curl

**Task 4: Create Weather Data Module** (30 min)
- Create `backend/weather.py`
- For now, use mock weather data based on scenario
- Later (Day 2) integrate Open-Meteo or OpenWeather API

**Deliverable**: Backend returns assets when calling `/scenario/run`

### Teammate B - AI & Frontend Lead

**Task 1: Set up Frontend Environment** (15 min)
```bash
cd frontend
npm install
```

**Task 2: Test Frontend Runs** (5 min)
```bash
npm start
# Should open http://localhost:3000
# You'll see the UI but no data yet (expected)
```

**Task 3: Test Frontend-Backend Connection** (20 min)
- Make sure backend is running (Task A.2)
- In frontend, click "Run Simulation" button
- Check browser console for errors
- Verify API calls are being made to `http://localhost:8000`

**Task 4: Draft LLM Prompt** (45 min)
- Create `backend/agent.py`
- Design system prompt for AI agent role:
  - Role: "You are an energy resilience planning agent..."
  - Input: scenario + risks + assets
  - Output: JSON with `summary_text` and `mitigation_actions[]`
- Define allowed `action_type` values (map to Beckn services)
- Use JSON mode in LLM API calls

**Deliverable**: 
- Frontend successfully calls backend API
- Agent prompt structure ready (implementation on Day 2)

## 📋 End of Day 1 Checklist

### Joint Review
- [ ] Both environments set up and running
- [ ] Backend returns assets from `/scenario/run`
- [ ] Frontend can call backend API
- [ ] No blocking errors in either side

### Code Review
- [ ] Review JSON contracts in `backend/main.py`
- [ ] Agree on action types for mitigation (e.g., "deploy_mobile_generator", "increase_cooling")
- [ ] Decide on LLM provider (OpenAI vs Claude)

## 🔜 Day 2 Preview

**Teammate A will:**
- Implement risk engine (`simulate_risk()` function)
- Complete `/scenario/run` with actual risk calculations
- Start mock Beckn functions

**Teammate B will:**
- Implement `/agent/mitigate` endpoint with LLM integration
- Complete frontend integration for displaying risks
- Add "Ask AI for Mitigation" button functionality

## 💡 Tips

1. **Keep it simple**: Focus on getting one thing working end-to-end first
2. **Use mock data**: Don't worry about real weather APIs yet
3. **Test frequently**: Run both backend and frontend often
4. **Communication**: Keep each other updated on API contract changes
5. **Version control**: Commit frequently with clear messages

## 🐛 Common Issues & Solutions

**Backend won't start:**
- Check Python version: `python --version` (need 3.10+)
- Make sure virtual environment is activated
- Try: `pip install --upgrade -r requirements.txt`

**Frontend can't connect to backend:**
- Check backend is running on port 8000
- Check CORS settings in `backend/main.py`
- Verify `API_BASE_URL` in `frontend/src/App.js`

**Import errors:**
- Make sure you're in the right directory
- Check virtual environment is activated (for Python)
- Try restarting the server

## 📞 Need Help?

- Review the plan document for architecture decisions
- Check `docs/API_CONTRACTS.md` for data formats
- Look at FastAPI docs: https://fastapi.tiangolo.com
- React docs: https://react.dev

Good luck! 🚀

