from fastapi import APIRouter, HTTPException, status
from app.schemas.order import OrderCreate, OrderResponse
from app.services.matching_engine import engine_manager

router = APIRouter(prefix="/orders", tags=["Trading"])

@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate):
    book = engine_manager.get_or_create_book(order.symbol)
    return book.match_order(order)

@router.get("/{symbol}/{order_id}", response_model=OrderResponse)
async def get_order(symbol: str, order_id: str):
    book = engine_manager.get_or_create_book(symbol)
    if order_id not in book.order_index:
        raise HTTPException(status_code=404, detail="Order not found")
    rec = book.order_index[order_id]
    return OrderResponse(**rec, execution_latency_us=0.0)
