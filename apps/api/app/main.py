import logging
import time
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from pythonjsonlogger import jsonlogger

# Logger setup
logger = logging.getLogger("finops-showback-tool-api")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

app = FastAPI(title="FinOps Showback Tool API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Path: {request.url.path} Duration: {duration:.4f}s Status: {response.status_code}")
    return response

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/billing/summary")
def get_billing_summary():
    return {
        "total_spend": 1250000.0,
        "allocated_spend": 1180000.0,
        "unallocated_spend": 70000.0,
        "allocation_pct": 94.4
    }

@app.post("/allocation/run")
def run_allocation(month: str = "2026-04"):
    logger.info(f"Running allocation engine for {month}")
    return {"status": "RUNNING", "job_id": f"alloc_{int(time.time())}", "month": month}

@app.get("/showback/by-team")
def get_showback_by_team():
    return [
        {"team": "Retail Platform", "direct": 450000, "shared": 12000, "total": 462000},
        {"team": "Markets Engine", "direct": 320000, "shared": 8500, "total": 328500},
        {"team": "Core Data", "direct": 180000, "shared": 15000, "total": 195000}
    ]

@app.get("/scores/summary")
def get_scores_summary():
    return {
        "showback_maturity": 78,
        "allocation_accuracy": 0.98,
        "forecast_accuracy": 0.92,
        "unit_economic_score": 0.65
    }

@app.get("/dashboard/summary")
def get_dashboard_summary():
    return {
        "active_connectors": 5,
        "last_sync": "2026-04-28T10:00:00Z",
        "open_disputes": 2,
        "maestro_status": "READY"
    }
