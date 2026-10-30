import pytest
from app.schemas.order import OrderCreate, OrderSide, OrderStatus
from app.services.matching_engine import MatchingEngineManager

def test_order_placement_and_retrieval():
    mgr = MatchingEngineManager()
    book = mgr.get_or_create_book("BTCUSDT")
    order = OrderCreate(symbol="BTCUSDT", side=OrderSide.BUY, price=68500.0, amount=0.5)
    resp = book.match_order(order)
    assert resp.symbol == "BTCUSDT"
    assert resp.status == OrderStatus.FILLED
    assert resp.order_id in book.order_index
