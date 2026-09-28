from contextlib import asynccontextmanager
import pandas as pd
from fastapi import FastAPI, Header, HTTPException
from prometheus_client import Counter, Histogram, generate_latest
from starlette.responses import Response
from fraud_detection.config.settings import get_settings
from fraud_detection.inference.predictor import FraudPredictor
from api.schemas import PredictionResponse, Transaction

settings = get_settings()
REQUESTS = Counter("fraud_api_requests_total", "Total prediction requests")
LATENCY = Histogram("fraud_api_latency_seconds", "Prediction latency")
predictor = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global predictor
    try: predictor = FraudPredictor(settings.model_dir)
    except Exception: predictor = None
    yield

app = FastAPI(title="Fraud Detection API", version="1.0.0", lifespan=lifespan)

@app.get("/health")
def health(): return {"status": "ok", "model_loaded": predictor is not None}

@app.get("/ready")
def ready():
    if predictor is None: raise HTTPException(503, "Model is not loaded")
    return {"status": "ready"}

@app.get("/metrics")
def metrics(): return Response(generate_latest(), media_type="text/plain")

@app.post("/predict", response_model=PredictionResponse)
def predict(transaction: Transaction, x_api_key: str | None = Header(default=None)):
    if settings.api_key != "change-me" and x_api_key != settings.api_key: raise HTTPException(401, "Invalid API key")
    if predictor is None: raise HTTPException(503, "Model is not loaded")
    REQUESTS.inc()
    with LATENCY.time():
        result = predictor.predict_frame(pd.DataFrame([transaction.model_dump()])).iloc[0]
    return PredictionResponse(**{k: result[k] for k in PredictionResponse.model_fields})
