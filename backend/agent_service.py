import os
import json
import google.generativeai as genai
from typing import List, Dict, Any

def configure_genai():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Warning: GOOGLE_API_KEY not found in environment variables")
        return
    genai.configure(api_key=api_key)

async def generate_mitigation_plan(request_data: Any) -> Dict[str, Any]:
    """
    Generate mitigation plan using Google Gemini.
    request_data: Instance of AgentMitigationRequest (passed as object)
    """
    configure_genai()
    
    # Extract data from request
    scenario = request_data.scenario
    risks = request_data.risks
    assets = request_data.assets
    
    # Construct prompt
    prompt = f"""
    You are an expert Distribution System Operator (DSO) Flexibility Orchestrator.
    Your goal is to manage grid congestion and prevent outages using Distributed Energy Resources (DERs) and Flexibility Services.
    
    Analyze the following grid scenario and identified risks.
    
    SCENARIO:
    Location: {scenario.location}
    Event: {scenario.event_type}
    Duration: {scenario.duration_hours} hours

    ASSETS:
    {json.dumps([a.model_dump() for a in assets], indent=2)}

    IDENTIFIED RISKS (Grid Constraints):
    {json.dumps([r.model_dump() for r in risks], indent=2)}

    TASK:
    Generate a Flexibility Dispatch Plan to address high and critical grid risks.
    Prioritize non-wires alternatives (Demand Response, Flexibility) over physical interventions.

    For each action, specify:
    - asset_id: The ID of the asset (feeder/substation) requiring relief
    - action_type: Specific flexibility service (MUST use one of: "dispatch_battery_discharge", "reduce_ev_load", "shift_hvac_load", "deploy_mobile_generator")
    - urgency: "low", "medium", or "high"
    - justification: Technical justification referencing load reduction (e.g., "Peak shaving required due to 110% projected loading")
    - target_time: A relative time string (e.g., "2025-11-26T10:00:00Z")

    RESPONSE FORMAT:
    Return ONLY a valid JSON object with two keys:
    1. "summary_text": A brief executive summary of the flexibility strategy.
    2. "mitigation_actions": A list of action objects matching the fields above.

    Example JSON:
    {{
        "summary_text": "Initiating peak shaving via VPP battery discharge to relieve substation overload...",
        "mitigation_actions": [
            {{
                "asset_id": "sub_1",
                "action_type": "dispatch_battery_discharge",
                "urgency": "high",
                "justification": "Projected load > 110% capacity due to AC spike",
                "target_time": "2025-11-26T14:00:00Z"
            }}
        ]
    }}
    """

    try:
        # Use gemini-flash-latest which is generally available
        model = genai.GenerativeModel('gemini-flash-latest')
        response = await model.generate_content_async(prompt)
        
        # Extract JSON from response
        content = response.text
        # Clean up markdown code blocks if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
            
        result = json.loads(content)
        
        # Validate structure minimally
        if "summary_text" not in result or "mitigation_actions" not in result:
            raise ValueError("Invalid response structure from AI")
            
        return result
        
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        # Fallback response
        return {
            "summary_text": f"Error generating AI plan: {str(e)}",
            "mitigation_actions": []
        }

