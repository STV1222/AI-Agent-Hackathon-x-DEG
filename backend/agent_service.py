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
    You are an expert in utility asset risk management and extreme weather resilience.
    Analyze the following scenario and risks to generate specific mitigation actions.

    SCENARIO:
    Location: {scenario.location}
    Event: {scenario.event_type}
    Duration: {scenario.duration_hours} hours

    ASSETS:
    {json.dumps([a.model_dump() for a in assets], indent=2)}

    IDENTIFIED RISKS:
    {json.dumps([r.model_dump() for r in risks], indent=2)}

    TASK:
    Generate a list of mitigation actions to address the high and critical risks.
    For each action, specify:
    - asset_id: The ID of the asset to protect
    - action_type: Specific action (e.g., "deploy_mobile_generator", "install_flood_barrier", "increase_cooling", "dispatch_repair_crew")
    - urgency: "low", "medium", or "high"
    - justification: Why this action is needed
    - target_time: A relative time string (e.g., "2025-11-26T10:00:00Z") - calculate based on start date {scenario.start_date} if possible, or just use a valid ISO timestamp.

    RESPONSE FORMAT:
    Return ONLY a valid JSON object with two keys:
    1. "summary_text": A brief text summary of the strategy.
    2. "mitigation_actions": A list of action objects matching the fields above.

    Example JSON:
    {{
        "summary_text": "Focus on protecting the substation from flooding...",
        "mitigation_actions": [
            {{
                "asset_id": "sub_1",
                "action_type": "deploy_sandbags",
                "urgency": "high",
                "justification": "Flood risk critical",
                "target_time": "2025-11-26T12:00:00Z"
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

