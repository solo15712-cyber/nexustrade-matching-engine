from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderType(str, Enum):
    LIMIT = "LIMIT"
    MARKET = "MARKET"

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"

class OrderCreate(BaseModel):
    symbol: str = Field(..., json_schema_extra={"example": "BTCUSDT"})
    side: OrderSide
    price: float = Field(..., gt=0, json_schema_extra={"example": 68500.0})
    amount: float = Field(..., gt=0, json_schema_extra={"example": 0.25})
    order_type: OrderType = OrderType.LIMIT

class OrderResponse(BaseModel):
    order_id: str
    symbol: str
    side: OrderSide
    price: float
    amount: float
    filled_amount: float
    status: OrderStatus
    timestamp_ns: int
    execution_latency_us: float
