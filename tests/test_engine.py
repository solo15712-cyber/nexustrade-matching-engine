import pytest
from fastapi.testclient import TestClient
from app.schemas.order import OrderCreate, OrderSide, OrderStatus
from app.services.matching_engine import MatchingEngineManager
from main import app

client = TestClient(app)

def test_order_placement_and_retrieval():
    mgr = MatchingEngineManager()
    book = mgr.get_or_create_book("BTCUSDT")
    order = OrderCreate(symbol="BTCUSDT", side=OrderSide.BUY, price=68500.0, amount=0.5)
    resp = book.match_order(order)
    assert resp.symbol == "BTCUSDT"
    assert resp.status == OrderStatus.FILLED
    assert resp.order_id in book.order_index

def test_order_sell_side():
    mgr = MatchingEngineManager()
    book = mgr.get_or_create_book("ETHUSDT")
    order = OrderCreate(symbol="ETHUSDT", side=OrderSide.SELL, price=3500.0, amount=2.0)
    resp = book.match_order(order)
    assert resp.symbol == "ETHUSDT"
    assert resp.side == OrderSide.SELL
    assert resp.status == OrderStatus.FILLED

def test_api_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"

def test_api_order_create_and_query():
    payload = {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "price": 69200.0,
        "amount": 0.1,
        "order_type": "LIMIT"
    }
    res_post = client.post("/api/v1/orders", json=payload)
    assert res_post.status_code == 201
    data = res_post.json()
    assert data["symbol"] == "BTCUSDT"
    assert "order_id" in data
    order_id = data["order_id"]

    # Query back
    res_get = client.get(f"/api/v1/orders/BTCUSDT/{order_id}")
    assert res_get.status_code == 200
    assert res_get.json()["order_id"] == order_id

def test_api_order_not_found():
    res = client.get("/api/v1/orders/BTCUSDT/non_existent_id")
    assert res.status_code == 404
    assert res.json()["detail"] == "Order not found"

def test_api_order_validation():
    # Price <= 0 should fail validation
    res = client.post("/api/v1/orders", json={"symbol": "BTCUSDT", "side": "BUY", "price": -100.0, "amount": 1.0})
    assert res.status_code == 422
