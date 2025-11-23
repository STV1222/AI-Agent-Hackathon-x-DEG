# Setup Guide - Extreme Weather Resilience Agent

## Prerequisites

- **Python 3.12+** (check with `python --version`)
- **Node.js 16+** and npm (check with `node --version` and `npm --version`)
- **uv** package manager (install with: `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **Google Gemini API Key** (get from: https://makersuite.google.com/app/apikey)

---

## Step 1: Get Your Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key (you'll need it in Step 3)

---

## Step 2: Backend Setup

### 2.1 Navigate to backend directory
```bash
cd backend
```

### 2.2 Install dependencies using uv
```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Python dependencies
uv sync
```

**Alternative (if uv doesn't work):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt  # Note: This file may not exist, use uv instead
```

### 2.3 Create .env file for API key

Create a file named `.env` in the `backend/` directory:

```bash
# In the backend directory
touch .env
```

Then add your Google API key to the `.env` file:
```
GOOGLE_API_KEY=your_actual_api_key_here
```

**Example:**
```
GOOGLE_API_KEY=AIzaSyAbc123Xyz456Def789Ghi012Jkl345Mno
```

**Important:** Replace `your_actual_api_key_here` with your actual API key from Step 1.

### 2.4 Activate virtual environment (if using venv)
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2.5 Run the backend server
```bash
# Using uv
uv run uvicorn main:app --reload

# OR if using venv
uvicorn main:app --reload
```

The backend will start on **http://localhost:8000**

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## Step 3: Frontend Setup

### 3.1 Open a NEW terminal window (keep backend running)

Navigate to frontend directory:
```bash
cd frontend
```

### 3.2 Install dependencies
```bash
npm install
```

### 3.3 Start the frontend
```bash
npm start
```

The frontend will start on **http://localhost:3000** and should open automatically in your browser.

---

## Step 4: Verify Everything Works

1. **Backend is running** - Check http://localhost:8000
   - You should see: `{"message": "Extreme Weather Resilience Agent API", "status": "running", ...}`

2. **Frontend is running** - Check http://localhost:3000
   - You should see the UI with scenario configuration panel

3. **Test the flow:**
   - Click a predefined scenario (e.g., "London Heatwave - 3 Days")
   - Wait for risks to appear
   - Click "Get AI Mitigation Plan" (requires API key)
   - Click "Execute via Beckn Network"

---

## Troubleshooting

### Backend Issues

**Problem:** `uv: command not found`
- **Solution:** Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Or use venv + pip instead

**Problem:** `GOOGLE_API_KEY not found`
- **Solution:** Make sure `.env` file exists in `backend/` directory with `GOOGLE_API_KEY=your_key`

**Problem:** Port 8000 already in use
- **Solution:** Change port: `uvicorn main:app --reload --port 8001`

**Problem:** Module not found errors
- **Solution:** Make sure you're in the backend directory and dependencies are installed

### Frontend Issues

**Problem:** `npm: command not found`
- **Solution:** Install Node.js from https://nodejs.org/

**Problem:** Port 3000 already in use
- **Solution:** React will automatically use the next available port (3001, 3002, etc.)

**Problem:** Cannot connect to backend
- **Solution:** Make sure backend is running on port 8000, or update `API_BASE_URL` in `frontend/src/App.js`

### API Key Issues

**Problem:** AI mitigation plan fails
- **Solution:** 
  1. Verify your API key is correct in `.env` file
  2. Make sure `.env` file is in `backend/` directory (not root)
  3. Restart the backend server after adding/changing `.env`

---

## Project Structure

```
AI_AGENT_HACKATHON/
├── backend/
│   ├── .env              # ← YOUR API KEY GOES HERE
│   ├── main.py           # FastAPI app
│   ├── agent_service.py  # AI agent (uses GOOGLE_API_KEY)
│   ├── pyproject.toml    # Dependencies
│   └── ...
├── frontend/
│   ├── src/
│   └── package.json
├── data/
│   ├── assets.json
│   └── scenarios.json
└── README.md
```

---

## Quick Start Commands Summary

**Terminal 1 (Backend):**
```bash
cd backend
uv sync
# Create .env file with GOOGLE_API_KEY=your_key
uv run uvicorn main:app --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm install
npm start
```

---

## Need Help?

- Check backend logs for errors
- Check browser console (F12) for frontend errors
- Verify API key is set correctly
- Make sure both servers are running

