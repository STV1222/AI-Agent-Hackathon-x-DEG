# Day 1 Checklist

## Joint Tasks (1-2 hours)

- [x] Project structure created
- [ ] Finalize scenarios (locations, events, asset types)
- [ ] Agree on stack (FastAPI backend, React frontend)
- [ ] Review JSON contracts (see API_CONTRACTS.md)
- [ ] Agree on agent responsibilities

## Teammate A - Backend & Data Lead

- [x] Backend skeleton created (FastAPI)
- [x] Mock DEG asset dataset ready (~20 assets in London)
- [x] Endpoints defined (empty implementations)
- [ ] Set up Python virtual environment
- [ ] Test backend runs on localhost:8000
- [ ] Create weather data module (start with hardcoded/mock)

## Teammate B - AI & Frontend Lead

- [x] Frontend skeleton created (React)
- [x] Basic layout and components structure
- [ ] Set up Node.js and install dependencies
- [ ] Test frontend runs on localhost:3000
- [ ] Draft initial LLM prompt (system prompt + JSON format)
- [ ] Review wireframe matches implemented layout

## End of Day 1 Goals

✅ Repo + skeleton backend & frontend  
✅ Asset mock data ready  
✅ Clear JSON contracts between backend ↔ AI ↔ frontend

## Next Steps (Day 2)

- Teammate A: Implement risk engine and `/scenario/run` endpoint
- Teammate B: Implement AI agent integration and `/agent/mitigate` endpoint

