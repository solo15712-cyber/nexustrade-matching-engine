# NexusTrade High-Concurrency Order Engine

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![Latency](https://img.shields.io/badge/Latency-p99%20<15us-brightgreen.svg)]()
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![Prometheus](https://img.shields.io/badge/Metrics-Prometheus-E6522C.svg)](https://prometheus.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Production-grade In-Memory Order Matching and Transaction Routing Engine engineered with FastAPI and Pydantic v2. Built for high-load financial exchanges, crypto order books, and real-time transaction processing.

## Architecture

```mermaid
flowchart TD
    Client["Client / Web / Mobile Frontends"] -->|"HTTP REST / WebSocket"| API["FastAPI Async Gateway (ASGI Workers)"]
    API -->|"Order Placement"| Engine["MatchingEngineManager"]
    Engine -->|"Sub-Microsecond Matching"| Book["In-Memory OrderBook (Dual Bids/Asks Index)"]
    API -->|"Metrics Scrape /metrics"| Prom["Prometheus Observability"]
    Engine -.->|"Market Depth Broadcast"| Redis[("Redis PubSub Buffer")]
    Engine -.->|"Async Audit & Settlement"| DB[("PostgreSQL Partitioned DB")]
```

## Benchmark Performance

Benchmark run on Linux host (5,000 order batch):
- **Throughput:** >60,000 orders/sec (Peak >120,000 orders/sec)
- **Latency (p50):** 5.37 microseconds (us)
- **Latency (p95):** 6.77 microseconds (us)
- **Latency (p99):** 8.23 microseconds (us)

## Production Observability & Endpoints

- `GET /health` -> JSON operational status and versioning.
- `GET /metrics` -> Native Prometheus telemetry scrape endpoint (order volume, active books, health).
- `POST /api/v1/orders` -> Real-time limit order placement and execution.
- `GET /api/v1/orders/{symbol}/{order_id}` -> Instant order status query.

## Quickstart & Docker Deployment

```bash
# Run unit and integration tests
pytest tests/ -v

# Run latency and throughput benchmark
python benchmark.py

# Deploy containerized stack with Docker Compose
docker-compose up -d --build
```

## Author
**Alireza Ghadiri** - Mid-Level Backend & Distributed Systems Engineer.
