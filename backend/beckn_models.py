from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

# ============================================================================
# Core Beckn Models
# ============================================================================

class Context(BaseModel):
    domain: str
    country: str = "GB"
    city: str = "std:020"  # London STD code example
    action: str  # search, on_search, select, on_select, etc.
    core_version: str = "0.9.3"
    bap_id: str
    bap_uri: str
    bpp_id: Optional[str] = None
    bpp_uri: Optional[str] = None
    transaction_id: str
    message_id: str
    timestamp: str  # ISO format
    ttl: Optional[str] = "PT30S"

# --- Shared Objects ---

class Descriptor(BaseModel):
    name: str
    code: Optional[str] = None
    symbol: Optional[str] = None
    short_desc: Optional[str] = None
    long_desc: Optional[str] = None
    images: Optional[List[str]] = None

class Price(BaseModel):
    currency: str
    value: str
    estimated_value: Optional[str] = None

class Item(BaseModel):
    id: str
    descriptor: Descriptor
    price: Optional[Price] = None
    category_id: Optional[str] = None
    fulfillment_id: Optional[str] = None

class Provider(BaseModel):
    id: str
    descriptor: Descriptor
    items: Optional[List[Item]] = None

class Fulfillment(BaseModel):
    id: str
    type: Optional[str] = "Delivery"
    tracking: bool = False

class Catalog(BaseModel):
    descriptor: Descriptor
    providers: List[Provider]

class Quote(BaseModel):
    price: Price
    breakup: Optional[List[Any]] = None

class Order(BaseModel):
    id: Optional[str] = None
    state: Optional[str] = None
    items: Optional[List[Item]] = None
    billing: Optional[Dict[str, Any]] = None
    fulfillment: Optional[Fulfillment] = None
    quote: Optional[Quote] = None
    payment: Optional[Dict[str, Any]] = None

# --- Intent & Message Bodies ---

class Intent(BaseModel):
    item: Optional[Dict[str, Any]] = None
    provider: Optional[Dict[str, Any]] = None
    fulfillment: Optional[Dict[str, Any]] = None
    category: Optional[Dict[str, Any]] = None

class SearchMessage(BaseModel):
    intent: Intent

class OnSearchMessage(BaseModel):
    catalog: Catalog

class SelectMessage(BaseModel):
    order: Order

class OnSelectMessage(BaseModel):
    order: Order
    quote: Optional[Quote] = None

class InitMessage(BaseModel):
    order: Order

class OnInitMessage(BaseModel):
    order: Order

class ConfirmMessage(BaseModel):
    order: Order

class OnConfirmMessage(BaseModel):
    order: Order

# --- API Request Wrappers ---

class BecknRequest(BaseModel):
    context: Context
    message: Dict[str, Any]  # Flexible to handle various message types

class SearchRequest(BaseModel):
    context: Context
    message: SearchMessage

class OnSearchRequest(BaseModel):
    context: Context
    message: OnSearchMessage

class SelectRequest(BaseModel):
    context: Context
    message: SelectMessage

class OnSelectRequest(BaseModel):
    context: Context
    message: OnSelectMessage

class ConfirmRequest(BaseModel):
    context: Context
    message: ConfirmMessage

class OnConfirmRequest(BaseModel):
    context: Context
    message: OnConfirmMessage

class Ack(BaseModel):
    status: str = "ACK"

class BecknResponse(BaseModel):
    message: Ack
    error: Optional[Dict[str, Any]] = None

