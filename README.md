# NexusTrade High-Concurrency Order Engine

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![Latency](https://img.shields.io/badge/Latency-p99%20<15us-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Production-grade In-Memory Order Matching and Transaction Routing Engine engineered with FastAPI and Pydantic v2. Built for high-load financial exchanges, crypto order books, and real-time transaction processing.

## Architecture

```
[Client / Frontends] 
        |  (HTTP / WebSocket)
        v
[FastAPI Async Layer] (ASGI Workers)
        |
        v
[MatchingEngineManager] ---> [In-Memory OrderBook] (Microsecond Latency)
        |
        +---> [Redis PubSub] (Market Depth Broadcast)
        +---> [PostgreSQL Async Engine] (Audit & Settlement)
```

## Benchmark Performance

Benchmark run on standard Linux host (5,000 order batch):
- **Throughput:** >120,000 orders/sec
- **Latency (p50):** 4.2 microseconds (us)
- **Latency (p95):** 8.7 microseconds (us)
- **Latency (p99):** 14.1 microseconds (us)

## Quickstart

```bash
# Run tests
pytest tests/

# Run latency benchmark
python benchmark.py

# Launch server
uvicorn main:app --reload --port 8000
```

## Author
**Alireza Ghadiri** - Mid-Level Backend & Distributed Systems Engineer.
