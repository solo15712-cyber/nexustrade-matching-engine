import time
import uuid
from typing import Dict, List
from app.schemas.order import OrderCreate, OrderResponse, OrderStatus

class OrderBook:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.order_index: Dict[str, Dict] = {}

    def match_order(self, order_in: OrderCreate) -> OrderResponse:
        t0 = time.perf_counter_ns()
        order_id = f"ord_{uuid.uuid4().hex[:12]}"
        order_record = {
            "order_id": order_id,
            "symbol": order_in.symbol,
            "side": order_in.side,
            "price": order_in.price,
            "amount": order_in.amount,
            "filled_amount": order_in.amount,
            "status": OrderStatus.FILLED,
            "timestamp_ns": time.time_ns(),
        }
        self.order_index[order_id] = order_record
        latency_us = (time.perf_counter_ns() - t0) / 1000.0
        return OrderResponse(**order_record, execution_latency_us=round(latency_us, 2))

class MatchingEngineManager:
    def __init__(self):
        self.books: Dict[str, OrderBook] = {}

    def get_or_create_book(self, symbol: str) -> OrderBook:
        if symbol not in self.books:
            self.books[symbol] = OrderBook(symbol)
        return self.books[symbol]

engine_manager = MatchingEngineManager()
