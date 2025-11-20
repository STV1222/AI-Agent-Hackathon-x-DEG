# Quick Start Guide

## Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- LLM API key (OpenAI or Anthropic Claude)

## Step 1: Backend Setup (Teammate A)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file and add your API keys
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY or ANTHROPIC_API_KEY

# Run backend server
uvicorn main:app --reload
```

Backend will run on `http://localhost:8000`

## Step 2: Frontend Setup (Teammate B)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will run on `http://localhost:3000`

## Step 3: Test the Setup

1. Open `http://localhost:3000` in your browser
2. Click one of the predefined scenarios (e.g., "London Heatwave - 3 Days")
3. You should see the map (though no data yet until Day 2 implementation)

## Troubleshooting

### Backend Issues
- Make sure port 8000 is not in use
- Check that all Python packages installed correctly
- Verify virtual environment is activated

### Frontend Issues
- Make sure port 3000 is not in use
- Clear `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Check browser console for errors

### API Connection
- Make sure backend is running before starting frontend
- Check CORS settings in `backend/main.py` if you see CORS errors
- Verify API_BASE_URL in `frontend/src/App.js` matches your backend URL

## Next Steps

See `docs/DAY1_CHECKLIST.md` for Day 1 tasks.

