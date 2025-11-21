import uuid
import httpx
from datetime import datetime
from typing import Dict, Any, Optional, List

from beckn_models import (
    Context, Intent, SearchRequest, SearchMessage,
    SelectRequest, SelectMessage, Order, Item,
    ConfirmRequest, ConfirmMessage
)

# --- In-Memory State Store (For Hackathon Simplicity) ---
# In production, use Redis/Database
# Structure: { transaction_id: { "status": "...", "catalog": ..., "quote": ..., "order": ... } }
BAP_STATE = {}

class BecknClient:
    def __init__(self, bap_id: str, bap_uri: str, bpp_uri: str):
        self.bap_id = bap_id
        self.bap_uri = bap_uri
        self.bpp_uri = bpp_uri  # Target BPP (Gateway or Specific BPP)

    def _create_context(self, action: str, transaction_id: str) -> Context:
        return Context(
            domain="energy-grid",
            action=action,
            bap_id=self.bap_id,
            bap_uri=self.bap_uri,
            transaction_id=transaction_id,
            message_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow().isoformat()
        )

    async def trigger_search(self, query: str, transaction_id: str) -> bool:
        """Send /search request to BPP"""
        context = self._create_context("search", transaction_id)
        
        # Initialize state
        BAP_STATE[transaction_id] = {
            "status": "SEARCH_INITIATED", 
            "last_update": datetime.utcnow()
        }
        
        payload = SearchRequest(
            context=context,
            message=SearchMessage(
                intent=Intent(
                    item={"descriptor": {"name": query}}
                )
            )
        )
        
        async with httpx.AsyncClient() as client:
            try:
                print(f"BAP: Sending search for '{query}'...")
                resp = await client.post(f"{self.bpp_uri}/search", json=payload.model_dump())
                if resp.status_code == 200:
                    return True
                print(f"BAP: Search failed with {resp.status_code}")
                return False
            except Exception as e:
                print(f"BAP: Connection error: {e}")
                return False

    async def trigger_select(self, transaction_id: str, provider_id: str, item_id: str) -> bool:
        """Send /select request"""
        context = self._create_context("select", transaction_id)
        
        # Retrieve provider details from state (assuming on_search populated it)
        # For simplicity, we just construct the item
        
        payload = SelectRequest(
            context=context,
            message=SelectMessage(
                order=Order(
                    items=[Item(id=item_id, descriptor={"name": "Selected Item"})] # simplified
                )
            )
        )
        
        async with httpx.AsyncClient() as client:
            try:
                print(f"BAP: Sending select for item {item_id}...")
                resp = await client.post(f"{self.bpp_uri}/select", json=payload.model_dump())
                return resp.status_code == 200
            except Exception as e:
                print(f"BAP: Connection error: {e}")
                return False

    async def trigger_confirm(self, transaction_id: str, item_id: str) -> bool:
        """Send /confirm request"""
        context = self._create_context("confirm", transaction_id)
        
        payload = ConfirmRequest(
            context=context,
            message=ConfirmMessage(
                order=Order(
                    items=[Item(id=item_id, descriptor={"name": "Confirmed Item"})],
                    billing={"name": "DEG Agent", "address": "London"},
                    fulfillment={"id": "ful_1", "type": "Delivery"}
                )
            )
        )
        
        async with httpx.AsyncClient() as client:
            try:
                print(f"BAP: Sending confirm...")
                resp = await client.post(f"{self.bpp_uri}/confirm", json=payload.model_dump())
                return resp.status_code == 200
            except Exception as e:
                print(f"BAP: Connection error: {e}")
                return False

