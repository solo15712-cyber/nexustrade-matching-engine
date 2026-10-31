from fastapi import FastAPI, Response
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.orders import router as orders_router
from app.services.matching_engine import engine_manager

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Ultra-Low Latency In-Memory Order Matching & FinTech Routing API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(orders_router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "operational", "version": settings.VERSION}

@app.get("/metrics", response_class=PlainTextResponse, tags=["Observability"])
async def prometheus_metrics():
    total_books = len(engine_manager.books)
    total_orders = sum(len(b.order_index) for b in engine_manager.books.values())
    metrics_payload = (
        "# HELP nexus_orders_total Total count of processed financial orders\n"
        "# TYPE nexus_orders_total counter\n"
        f"nexus_orders_total {total_orders}\n"
        "# HELP nexus_active_order_books Total active symbol books in memory\n"
        "# TYPE nexus_active_order_books gauge\n"
        f"nexus_active_order_books {total_books}\n"
        "# HELP nexus_engine_health Status of high-concurrency engine (1=healthy)\n"
        "# TYPE nexus_engine_health gauge\n"
        "nexus_engine_health 1\n"
    )
    return Response(content=metrics_payload, media_type="text/plain; version=0.0.4; charset=utf-8")
