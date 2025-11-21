from fastapi import APIRouter, BackgroundTasks
from datetime import datetime
import asyncio
import httpx
import uuid
from typing import Dict, Any

from beckn_models import (
    SearchRequest, SelectRequest, ConfirmRequest, 
    BecknResponse, Ack, OnSearchRequest, OnSearchMessage,
    OnSelectRequest, OnSelectMessage, OnConfirmRequest, OnConfirmMessage,
    Catalog, Descriptor, Provider, Item, Price, Quote, Order, Fulfillment,
    Context
)

router = APIRouter(prefix="/mock-bpp", tags=["Mock BPP"])

# Mock Data Inventory
INVENTORY = {
    "deploy_mobile_generator": [
        {"id": "gen_100kw", "name": "100kW Mobile Generator", "price": "150.0", "desc": "Diesel generator on trailer"},
        {"id": "gen_500kw", "name": "500kW Power Unit", "price": "600.0", "desc": "Industrial grade power unit"}
    ],
    "increase_cooling": [
        {"id": "chiller_port", "name": "Portable Chiller", "price": "200.0", "desc": "Air cooled chiller 50 ton"},
        {"id": "spot_cool", "name": "Spot Cooler", "price": "50.0", "desc": "5 ton spot cooler"}
    ],
    "fallback": [
        {"id": "generic_service", "name": "General Service", "price": "100.0", "desc": "Standard service request"}
    ]
}

# --- Background Tasks (Simulating Async Processing) ---

async def process_search(request: SearchRequest):
    """Simulate search processing and send callback"""
    await asyncio.sleep(2)  # Simulate network/db latency
    
    # Extract query
    intent = request.message.intent
    query_item_name = ""
    if intent.item and "descriptor" in intent.item:
         query_item_name = intent.item["descriptor"].get("name", "")
    
    # Match inventory (simple string match or fallback)
    matched_items = []
    
    # Simplified matching logic
    inv_key = "fallback"
    for key in INVENTORY.keys():
        if key in query_item_name:
            inv_key = key
            break
            
    for prod in INVENTORY[inv_key]:
        matched_items.append(Item(
            id=prod["id"],
            descriptor=Descriptor(name=prod["name"], short_desc=prod["desc"]),
            price=Price(currency="GBP", value=prod["price"]),
            fulfillment_id="ful_1"
        ))
    
    # Construct Response
    response_context = request.context.model_copy()
    response_context.action = "on_search"
    response_context.bpp_id = "mock-bpp-london"
    response_context.bpp_uri = "http://localhost:8000/mock-bpp"
    response_context.timestamp = datetime.utcnow().isoformat()
    
    catalog = Catalog(
        descriptor=Descriptor(name="Mock BPP Catalog"),
        providers=[
            Provider(
                id="prov_mock_1",
                descriptor=Descriptor(name="Mock Provider Services"),
                items=matched_items
            )
        ]
    )
    
    on_search_payload = OnSearchRequest(
        context=response_context,
        message=OnSearchMessage(catalog=catalog)
    )
    
    # Send Callback
    async with httpx.AsyncClient() as client:
        try:
            # The BAP URI from the request context
            target_uri = f"{request.context.bap_uri}/on_search" 
            # If local dev, ensure we hit the right endpoint
            if "localhost" in request.context.bap_uri and "/beckn" not in target_uri:
                 # Fix potential path issue if bap_uri is just base url
                 pass 
                 
            print(f"BPP: Sending on_search to {target_uri}")
            await client.post(target_uri, json=on_search_payload.model_dump())
        except Exception as e:
            print(f"BPP: Callback failed: {e}")

async def process_select(request: SelectRequest):
    """Simulate selection and quote generation"""
    await asyncio.sleep(1)
    
    response_context = request.context.model_copy()
    response_context.action = "on_select"
    response_context.bpp_id = "mock-bpp-london"
    response_context.bpp_uri = "http://localhost:8000/mock-bpp"
    response_context.timestamp = datetime.utcnow().isoformat()
    
    # Generate Quote
    order_items = request.message.order.items or []
    total_val = 0.0
    for item in order_items:
        # Simple mock pricing logic
        total_val += 150.0 # assume generic price if not found
        
    quote = Quote(
        price=Price(currency="GBP", value=str(total_val)),
        breakup=[
            {"title": "Item Total", "price": {"currency": "GBP", "value": str(total_val)}}
        ]
    )
    
    on_select_payload = OnSelectRequest(
        context=response_context,
        message=OnSelectMessage(
            order=Order(items=order_items, quote=quote)
        )
    )
    
    async with httpx.AsyncClient() as client:
        try:
            target_uri = f"{request.context.bap_uri}/on_select"
            print(f"BPP: Sending on_select to {target_uri}")
            await client.post(target_uri, json=on_select_payload.model_dump())
        except Exception as e:
            print(f"BPP: Callback failed: {e}")

async def process_confirm(request: ConfirmRequest):
    """Simulate order confirmation"""
    await asyncio.sleep(1)
    
    response_context = request.context.model_copy()
    response_context.action = "on_confirm"
    response_context.bpp_id = "mock-bpp-london"
    response_context.bpp_uri = "http://localhost:8000/mock-bpp"
    response_context.timestamp = datetime.utcnow().isoformat()
    
    # Create confirmed order
    order = request.message.order
    order.id = f"ORD-{uuid.uuid4().hex[:8]}"
    order.state = "Created"
    
    on_confirm_payload = OnConfirmRequest(
        context=response_context,
        message=OnConfirmMessage(order=order)
    )
    
    async with httpx.AsyncClient() as client:
        try:
            target_uri = f"{request.context.bap_uri}/on_confirm"
            print(f"BPP: Sending on_confirm to {target_uri}")
            await client.post(target_uri, json=on_confirm_payload.model_dump())
        except Exception as e:
            print(f"BPP: Callback failed: {e}")


# --- Endpoints ---

@router.post("/search", response_model=BecknResponse)
async def search(request: SearchRequest, background_tasks: BackgroundTasks):
    print(f"BPP: Received search request: {request.message.intent}")
    background_tasks.add_task(process_search, request)
    return BecknResponse(message=Ack())

@router.post("/select", response_model=BecknResponse)
async def select(request: SelectRequest, background_tasks: BackgroundTasks):
    print(f"BPP: Received select request")
    background_tasks.add_task(process_select, request)
    return BecknResponse(message=Ack())

@router.post("/confirm", response_model=BecknResponse)
async def confirm(request: ConfirmRequest, background_tasks: BackgroundTasks):
    print(f"BPP: Received confirm request")
    background_tasks.add_task(process_confirm, request)
    return BecknResponse(message=Ack())

