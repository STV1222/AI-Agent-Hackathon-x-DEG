import asyncio
import uuid
from datetime import datetime
from typing import Dict, Any, List

from beckn_bap import BecknClient, BAP_STATE

# Configure Client
# In production, these would be env vars
BAP_ID = "deg-agent-bap"
BAP_URI = "http://localhost:8000/beckn"  # Must be reachable by BPP
BPP_URI = "http://localhost:8000/mock-bpp" # Target Gateway/BPP

client = BecknClient(BAP_ID, BAP_URI, BPP_URI)

async def poll_for_status(transaction_id: str, target_status: str, timeout: int = 10) -> bool:
    """Poll state until status reached or timeout"""
    start_time = datetime.utcnow()
    while (datetime.utcnow() - start_time).total_seconds() < timeout:
        state = BAP_STATE.get(transaction_id)
        if state and state.get("status") == target_status:
            return True
        await asyncio.sleep(0.5)
    return False

async def execute_beckn_flow(action_type: str, location: str) -> Dict[str, Any]:
    """
    Orchestrate the full Beckn flow for a single action:
    Search -> (Wait) -> Select -> (Wait) -> Confirm -> (Wait)
    """
    transaction_id = str(uuid.uuid4())
    print(f"Orchestrator: Starting flow {transaction_id} for {action_type}")
    
    # 1. Trigger Search
    sent = await client.trigger_search(action_type, transaction_id)
    if not sent:
        return {"status": "failed", "reason": "Search request failed"}
        
    # 2. Wait for on_search
    if not await poll_for_status(transaction_id, "SEARCH_COMPLETED"):
         return {"status": "failed", "reason": "Search timeout or no providers"}
    
    # 3. Process Catalog & Select Best
    catalog = BAP_STATE[transaction_id].get("catalog")
    if not catalog or not catalog.providers:
         return {"status": "failed", "reason": "No providers returned in catalog"}
         
    # Simple logic: pick first item from first provider
    provider = catalog.providers[0]
    item = provider.items[0]
    
    # 4. Trigger Select
    sent = await client.trigger_select(transaction_id, provider.id, item.id)
    if not sent:
        return {"status": "failed", "reason": "Select request failed"}
        
    # 5. Wait for on_select
    if not await poll_for_status(transaction_id, "SELECT_COMPLETED"):
        return {"status": "failed", "reason": "Select timeout"}
        
    # 6. Trigger Confirm
    sent = await client.trigger_confirm(transaction_id, item.id)
    if not sent:
        return {"status": "failed", "reason": "Confirm request failed"}
        
    # 7. Wait for on_confirm
    if not await poll_for_status(transaction_id, "CONFIRM_COMPLETED"):
        return {"status": "failed", "reason": "Confirm timeout"}
        
    # Success!
    confirmed_order = BAP_STATE[transaction_id].get("confirmed_order")
    
    return {
        "status": "confirmed",
        "provider": provider.descriptor.name,
        "details": f"Order ID: {confirmed_order.id}, State: {confirmed_order.state}",
        "transaction_id": transaction_id
    }
