import time
import statistics
from app.schemas.order import OrderCreate, OrderSide
from app.services.matching_engine import engine_manager

def run_benchmark(num_orders: int = 5000):
    book = engine_manager.get_or_create_book("BTCUSDT")
    latencies = []
    print(f"[BENCHMARK] Executing {num_orders:,} orders...")
    t_start = time.perf_counter()
    for i in range(num_orders):
        order = OrderCreate(
            symbol="BTCUSDT",
            side=OrderSide.BUY if i % 2 == 0 else OrderSide.SELL,
            price=68000.0 + (i % 100),
            amount=0.1 + (i % 5) * 0.05
        )
        resp = book.match_order(order)
        latencies.append(resp.execution_latency_us)
    total_duration = time.perf_counter() - t_start
    rps = num_orders / total_duration
    latencies.sort()
    p50 = statistics.median(latencies)
    p95 = latencies[int(len(latencies) * 0.95)]
    p99 = latencies[int(len(latencies) * 0.99)]
    print(f"[RESULTS] RPS: {rps:,.0f} | p50: {p50:.2f}us | p95: {p95:.2f}us | p99: {p99:.2f}us")

if __name__ == '__main__':
    run_benchmark(5000)
