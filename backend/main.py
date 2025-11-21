"""
Extreme Weather Resilience Agent - Backend API
FastAPI application for risk simulation and AI agent orchestration
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

from utils import load_assets
from weather import get_weather_for_scenario
from risk_engine import simulate_risk
from agent_service import generate_mitigation_plan
from beckn_service import execute_beckn_flow

app = FastAPI(
    title="Extreme Weather Resilience Agent API",
    description="AI agent for DEG asset risk simulation and mitigation orchestration",
    version="0.1.0"
)

# CORS middleware for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Pydantic Models (JSON Contracts)
# ============================================================================

class ScenarioRequest(BaseModel):
    location: str  # e.g., "London"
    event_type: str  # "heatwave" or "flood"
    start_date: str  # ISO format: "2025-11-26T00:00:00Z"
    duration_hours: int


class Asset(BaseModel):
    id: str
    name: str
    type: str  # "substation", "ev_hub", "solar_farm"
    lat: float
    lon: float
    capacity_kw: float
    criticality: str  # "low", "medium", "high"


class RiskResult(BaseModel):
    asset_id: str
    risk_level: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    reason: str
    expected_impact: str


class ScenarioResponse(BaseModel):
    scenario: ScenarioRequest
    assets: List[Asset]
    risks: List[RiskResult]


class MitigationAction(BaseModel):
    asset_id: str
    action_type: str  # "deploy_mobile_generator", "increase_cooling", etc.
    urgency: str  # "low", "medium", "high"
    justification: str
    target_time: str  # ISO format


class AgentMitigationRequest(BaseModel):
    scenario: ScenarioRequest
    risks: List[RiskResult]
    assets: List[Asset]


class AgentMitigationResponse(BaseModel):
    summary_text: str
    mitigation_actions: List[MitigationAction]


class BecknServiceResult(BaseModel):
    provider_id: str
    name: str
    eta_hours: int
    price_estimate: float


class BecknSearchResult(BaseModel):
    service_type: str
    results: List[BecknServiceResult]


class BecknExecutionLog(BaseModel):
    asset_id: str
    service_type: str
    provider: Optional[str]
    status: str  # "searched", "confirmed", "failed"


class BecknExecutionRequest(BaseModel):
    actions: List[MitigationAction]


class BecknExecutionResponse(BaseModel):
    log: List[BecknExecutionLog]


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/")
def root():
    return {
        "message": "Extreme Weather Resilience Agent API",
        "status": "running",
        "endpoints": {
            "scenario": "/scenario/run",
            "agent": "/agent/mitigate",
            "beckn": "/beckn/execute"
        }
    }


@app.post("/scenario/run", response_model=ScenarioResponse)
async def run_scenario(scenario: ScenarioRequest):
    """
    Run risk simulation for a given weather scenario.
    
    Loads DEG assets for the location, fetches weather data, and runs risk simulation.
    """
    # Load assets for the location
    assets_data = load_assets(scenario.location)
    
    # Get weather data for the scenario
    weather_data = get_weather_for_scenario(scenario)
    
    # Run risk simulation
    risk_results = simulate_risk(scenario.event_type, weather_data, assets_data)
    
    # Convert to Pydantic models
    assets = [Asset(**asset) for asset in assets_data]
    risks = [RiskResult(**risk) for risk in risk_results]
    
    return ScenarioResponse(
        scenario=scenario,
        assets=assets,
        risks=risks
    )


@app.post("/agent/mitigate", response_model=AgentMitigationResponse)
async def get_mitigation_plan(request: AgentMitigationRequest):
    """
    Call AI agent to generate mitigation plan based on risk results.
    
    Uses Google Gemini to analyze scenario and risks.
    """
    # Call Agent Service
    agent_result = await generate_mitigation_plan(request)
    
    # Convert dict result to Pydantic model
    return AgentMitigationResponse(**agent_result)


@app.post("/beckn/execute", response_model=BecknExecutionResponse)
async def execute_beckn_services(request: BecknExecutionRequest):
    """
    Simulate Beckn-style service search and confirmation for mitigation actions.
    """
    logs = []
    
    # Process each action
    for action in request.actions:
        # Execute Beckn flow (Search -> Select -> Confirm)
        # We assume "location" is implicitly known or passed (using "London" default here for simplicity 
        # or we could extract from action if needed, but action doesn't have location. 
        # Real implementation would pass context.)
        result = await execute_beckn_flow(action.action_type, "London")
        
        # Create log entry
        log_entry = BecknExecutionLog(
            asset_id=action.asset_id,
            service_type=action.action_type,
            provider=result.get("provider"),
            status=result.get("status", "failed")
        )
        logs.append(log_entry)
        
    return BecknExecutionResponse(
        log=logs
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

