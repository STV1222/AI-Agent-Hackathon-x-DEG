import random
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime

# Mock Providers Database
MOCK_PROVIDERS = {
    "deploy_mobile_generator": [
        {"id": "prov_gen_1", "name": "FastPower Inc", "base_eta": 4, "price_per_hour": 150.0},
        {"id": "prov_gen_2", "name": "LocalGrid Support", "base_eta": 2, "price_per_hour": 180.0},
        {"id": "prov_gen_3", "name": "Emergency Power Co", "base_eta": 6, "price_per_hour": 120.0}
    ],
    "increase_cooling": [
        {"id": "prov_cool_1", "name": "CoolTech Solutions", "base_eta": 6, "price_per_hour": 200.0},
        {"id": "prov_cool_2", "name": "HVAC Masters", "base_eta": 3, "price_per_hour": 250.0}
    ],
    "deploy_sandbags": [
        {"id": "prov_flood_1", "name": "FloodDefense Corp", "base_eta": 5, "price_per_hour": 80.0},
        {"id": "prov_flood_2", "name": "City Works Dept", "base_eta": 12, "price_per_hour": 50.0}
    ],
    "dispatch_repair_crew": [
        {"id": "prov_crew_1", "name": "GridFix Squad", "base_eta": 1, "price_per_hour": 300.0},
        {"id": "prov_crew_2", "name": "Rapid Response Unit", "base_eta": 2, "price_per_hour": 280.0}
    ]
}

async def search_services(action_type: str, location: str) -> List[Dict[str, Any]]:
    """
    Simulate searching for services on the Beckn network.
    Returns a list of provider offers.
    """
    # Simulate network latency
    await asyncio.sleep(0.5)
    
    # Find matching providers (or generic fallback)
    providers = MOCK_PROVIDERS.get(action_type)
    if not providers:
        # Fallback for unknown action types
        return [
            {
                "provider_id": "prov_generic_1", 
                "name": "General Services Ltd", 
                "eta_hours": 24, 
                "price_estimate": 100.0
            }
        ]
    
    # Add some variability to results to simulate real-time conditions
    results = []
    for p in providers:
        # Randomize ETA slightly based on location (mock logic)
        eta = p["base_eta"] + random.randint(-1, 2)
        if eta < 1: eta = 1
        
        results.append({
            "provider_id": p["id"],
            "name": p["name"],
            "eta_hours": eta,
            "price_estimate": p["price_per_hour"]
        })
    
    return results

async def select_and_confirm(provider_id: str) -> bool:
    """
    Simulate the Select and Confirm steps of Beckn protocol.
    Returns True if confirmed, False otherwise.
    """
    # Simulate processing time
    await asyncio.sleep(0.3)
    
    # Mock success rate (90% success)
    return random.random() < 0.9

async def execute_beckn_flow(action_type: str, location: str) -> Dict[str, Any]:
    """
    Orchestrate the full Beckn flow for a single action:
    1. Search
    2. Select best option (lowest ETA)
    3. Confirm
    """
    # 1. Search
    offers = await search_services(action_type, location)
    if not offers:
        return {
            "status": "failed",
            "reason": "No providers found",
            "provider": None
        }
        
    # 2. Select (Strategy: Minimize ETA)
    offers.sort(key=lambda x: x["eta_hours"])
    best_offer = offers[0]
    
    # 3. Confirm
    confirmed = await select_and_confirm(best_offer["provider_id"])
    
    if confirmed:
        return {
            "status": "confirmed",
            "provider": best_offer["name"],
            "details": f"ETA: {best_offer['eta_hours']}h, Price: ${best_offer['price_estimate']}/hr"
        }
    else:
        return {
            "status": "failed",
            "reason": "Provider declined booking",
            "provider": best_offer["name"]
        }

