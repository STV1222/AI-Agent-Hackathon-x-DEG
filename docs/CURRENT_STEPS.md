# What to Do Now - Step by Step Guide

## ✅ What's Been Done

1. ✅ **Backend `/scenario/run` endpoint** - Now loads assets and calculates risks
2. ✅ **Risk Engine** - Basic risk calculation based on weather thresholds
3. ✅ **Weather Module** - Mock weather data for scenarios
4. ✅ **Frontend** - Already set up and ready

## 🎯 Next Steps

### Step 1: Test the Basic Flow (5 minutes)

1. **Make sure backend is running:**
   ```bash
   cd backend
   source venv/bin/activate  # if not already activated
   uvicorn main:app --reload
   ```

2. **Make sure frontend is running:**
   ```bash
   cd frontend
   npm start
   ```

3. **Test in browser:**
   - Open http://localhost:3000
   - Click "London Heatwave - 3 Days" button
   - **Expected result**: 
     - Map should show assets (colored dots)
     - Right panel should show risk assessment with affected assets
     - Assets should be colored by risk level (red=critical, orange=high, yellow=medium)

4. **If you see assets and risks** → Great! Move to Step 2
5. **If not working** → Check:
   - Browser console for errors (F12)
   - Backend terminal for errors
   - Make sure backend is on port 8000
   - Make sure frontend is on port 3000

---

### Step 2: Implement AI Agent Endpoint (30-45 minutes)

**Task**: Implement `/agent/mitigate` endpoint that calls an LLM to generate mitigation plans.

**File to edit**: `backend/main.py` and create `backend/agent.py`

**Steps**:

1. **Create `backend/agent.py`** with LLM integration:

```python
import json
import os
from typing import List, Dict, Any

# Choose one: OpenAI or Anthropic
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

def call_ai_agent(scenario: Dict, risks: List[Dict], assets: List[Dict]) -> Dict:
    """
    Call LLM to generate mitigation plan.
    """
    # Format prompt
    prompt = format_mitigation_prompt(scenario, risks, assets)
    
    # Call LLM (example with OpenAI)
    if OPENAI_API_KEY:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # or "gpt-4"
            messages=[
                {"role": "system", "content": get_system_prompt()},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}  # Force JSON output
        )
        result = json.loads(response.choices[0].message.content)
        return result
    # Or use Anthropic Claude similarly
    
    # Fallback if no API key
    return {
        "summary_text": "AI agent not configured. Please add API key.",
        "mitigation_actions": []
    }

def get_system_prompt() -> str:
    return """You are an energy resilience planning agent for the Digital Energy Grid (DEG).
Your role is to analyze weather-related risks to energy infrastructure and recommend mitigation actions.

You must respond in JSON format with:
- "summary_text": A human-readable explanation of the risks and mitigation strategy
- "mitigation_actions": A list of actions, each with:
  - "asset_id": The ID of the asset
  - "action_type": One of: "deploy_mobile_generator", "increase_cooling", "prepare_flood_protection", "reduce_load", "monitor_asset"
  - "urgency": "low", "medium", or "high"
  - "justification": Why this action is needed
  - "target_time": ISO format timestamp for when action should be taken

Prioritize critical assets (hospitals, transport hubs) and CRITICAL/HIGH risk levels."""

def format_mitigation_prompt(scenario: Dict, risks: List[Dict], assets: List[Dict]) -> str:
    """Format the user prompt with scenario and risk data."""
    # Build prompt with scenario info and top risks
    top_risks = risks[:10]  # Top 10 risks
    
    prompt = f"""Analyze this extreme weather scenario and recommend mitigation actions:

SCENARIO:
- Location: {scenario.get('location')}
- Event Type: {scenario.get('event_type')}
- Duration: {scenario.get('duration_hours')} hours
- Start: {scenario.get('start_date')}

RISKS DETECTED:
{json.dumps(top_risks, indent=2)}

ASSETS AFFECTED:
{json.dumps([a for a in assets if any(r['asset_id'] == a['id'] for r in risks)], indent=2)}

Provide a mitigation plan with specific actions for each high-risk asset."""
    
    return prompt
```

2. **Update `backend/main.py`** to use the agent:

```python
from agent import call_ai_agent

@app.post("/agent/mitigate", response_model=AgentMitigationResponse)
async def get_mitigation_plan(request: AgentMitigationRequest):
    # Convert Pydantic models to dicts for processing
    scenario_dict = request.scenario.dict()
    risks_dict = [risk.dict() for risk in request.risks]
    assets_dict = [asset.dict() for asset in request.assets]
    
    # Call AI agent
    result = call_ai_agent(scenario_dict, risks_dict, assets_dict)
    
    # Convert back to Pydantic models
    actions = [MitigationAction(**action) for action in result.get("mitigation_actions", [])]
    
    return AgentMitigationResponse(
        summary_text=result.get("summary_text", ""),
        mitigation_actions=actions
    )
```

3. **Add API key to `.env` file**:
   ```bash
   cd backend
   # Create .env file (copy from .env.example if exists, or create new)
   echo "OPENAI_API_KEY=your_key_here" > .env
   # OR
   echo "ANTHROPIC_API_KEY=your_key_here" > .env
   ```

4. **Test**:
   - Run a scenario in frontend
   - Click "Get AI Mitigation Plan" button
   - Should see AI explanation and recommended actions

---

### Step 3: Implement Mock Beckn Functions (20-30 minutes)

**Task**: Implement `/beckn/execute` endpoint that simulates Beckn network service calls.

**File to edit**: Create `backend/beckn.py` and update `backend/main.py`

**Steps**:

1. **Create `backend/beckn.py`**:

```python
import random
from typing import List, Dict, Any

# Mock service providers database
MOCK_PROVIDERS = {
    "deploy_mobile_generator": [
        {"provider_id": "GENSET_UK_01", "name": "UK Mobile Gensets Ltd", "eta_hours": 4, "price_estimate": 1200},
        {"provider_id": "GENSET_UK_02", "name": "Power Solutions UK", "eta_hours": 6, "price_estimate": 1000},
    ],
    "increase_cooling": [
        {"provider_id": "COOL_UK_01", "name": "Cooling Systems Ltd", "eta_hours": 2, "price_estimate": 500},
        {"provider_id": "COOL_UK_02", "name": "Industrial Cooling Services", "eta_hours": 3, "price_estimate": 450},
    ],
    "prepare_flood_protection": [
        {"provider_id": "FLOOD_UK_01", "name": "Flood Defense Services", "eta_hours": 6, "price_estimate": 800},
        {"provider_id": "FLOOD_UK_02", "name": "Emergency Protection Ltd", "eta_hours": 4, "price_estimate": 950},
    ],
    "reduce_load": [
        {"provider_id": "LOAD_UK_01", "name": "Load Management Services", "eta_hours": 1, "price_estimate": 300},
    ],
    "monitor_asset": [
        {"provider_id": "MON_UK_01", "name": "Grid Monitoring Systems", "eta_hours": 0, "price_estimate": 200},
    ],
}

def beckn_search(service_type: str, location: str) -> List[Dict[str, Any]]:
    """Simulate Beckn network search for service providers."""
    providers = MOCK_PROVIDERS.get(service_type, [])
    
    # Simulate network latency
    # In real implementation, this would call Beckn network APIs
    
    return providers

def beckn_select_and_confirm(service_type: str, provider_id: str, action: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate Beckn network select and confirm flow."""
    # Find provider
    providers = MOCK_PROVIDERS.get(service_type, [])
    provider = next((p for p in providers if p["provider_id"] == provider_id), None)
    
    if not provider:
        return {"status": "failed", "reason": "Provider not found"}
    
    # Simulate confirmation
    # In real implementation, this would call Beckn confirm API
    
    return {
        "status": "confirmed",
        "provider": provider,
        "asset_id": action.get("asset_id"),
        "service_type": service_type
    }

def execute_beckn_actions(actions: List[Dict[str, Any]], location: str = "London") -> List[Dict[str, Any]]:
    """Execute Beckn network calls for a list of mitigation actions."""
    log = []
    
    for action in actions:
        service_type = action.get("action_type")
        asset_id = action.get("asset_id")
        
        # Step 1: Search for providers
        providers = beckn_search(service_type, location)
        
        if not providers:
            log.append({
                "asset_id": asset_id,
                "service_type": service_type,
                "provider": None,
                "status": "failed",
                "reason": "No providers found"
            })
            continue
        
        # Step 2: Select best provider (e.g., fastest ETA)
        selected_provider = min(providers, key=lambda p: p["eta_hours"])
        
        # Step 3: Confirm booking
        confirmation = beckn_select_and_confirm(service_type, selected_provider["provider_id"], action)
        
        log.append({
            "asset_id": asset_id,
            "service_type": service_type,
            "provider": selected_provider["provider_id"],
            "status": confirmation["status"]
        })
    
    return log
```

2. **Update `backend/main.py`**:

```python
from beckn import execute_beckn_actions

@app.post("/beckn/execute", response_model=BecknExecutionResponse)
async def execute_beckn_services(request: BecknExecutionRequest):
    # Convert to dicts
    actions_dict = [action.dict() for action in request.actions]
    
    # Execute Beckn calls
    log = execute_beckn_actions(actions_dict)
    
    # Convert to Pydantic models
    log_entries = [BecknExecutionLog(**entry) for entry in log]
    
    return BecknExecutionResponse(log=log_entries)
```

3. **Test**:
   - Get AI mitigation plan
   - Click "Execute via Beckn Network" button
   - Should see Beckn activity log at bottom showing confirmed services

---

## 🎉 Full Flow Test

Once all steps are done, test the complete flow:

1. **Run Scenario**: Click "London Heatwave - 3 Days"
   - ✅ See assets on map
   - ✅ See risks in right panel

2. **Get AI Plan**: Click "Get AI Mitigation Plan"
   - ✅ See AI explanation
   - ✅ See recommended actions

3. **Execute Beckn**: Click "Execute via Beckn Network"
   - ✅ See Beckn log with confirmed services
   - ✅ See provider names and statuses

## 🐛 Troubleshooting

**Backend errors:**
- Check all imports are correct
- Make sure virtual environment is activated
- Check API keys are set if using LLM

**Frontend not showing data:**
- Open browser console (F12)
- Check Network tab for API calls
- Verify CORS is working (check backend terminal)

**LLM not responding:**
- Verify API key is correct in `.env`
- Check API quota/limits
- Test API key works: `python -c "from openai import OpenAI; print(OpenAI().models.list())"`

## 📝 Next: Day 2 Tasks

After completing Steps 1-3, you'll have a working demo! Then you can:
- Polish UI/UX
- Add more scenarios
- Refine risk engine
- Add more service types
- Prepare pitch deck

Good luck! 🚀

