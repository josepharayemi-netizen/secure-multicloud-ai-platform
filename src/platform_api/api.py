import os
import time
import uuid
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from prometheus_client import Counter, Histogram, make_asgi_app
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from .features import Transaction
from .service import RiskService

app = FastAPI(title="Secure Multi-Cloud AI Platform", version="2.0.0")
service = RiskService()
REQUESTS = Counter("ai_inference_requests_total", "Inference requests", ["decision"])
LATENCY = Histogram("ai_inference_latency_seconds", "Inference latency")
app.mount("/metrics", make_asgi_app())


def configure_tracing() -> None:
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if not endpoint:
        return
    provider = TracerProvider(resource=Resource.create({"service.name": "secure-ai-api"}))
    provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=f"{endpoint.rstrip('/')}/v1/traces")))
    trace.set_tracer_provider(provider)
    FastAPIInstrumentor.instrument_app(app)


configure_tracing()


class PredictionRequest(BaseModel):
    transaction_amount: float = Field(gt=0, le=10_000_000)
    velocity_1h: int = Field(ge=0, le=1000)
    account_age_days: int = Field(ge=0, le=36500)
    country_mismatch: bool


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Cache-Control"] = "no-store"
    return response


@app.get("/health/live")
def live():
    return {"status": "alive"}


@app.get("/health/ready")
def ready():
    return {"status": "ready", "model_version": service.metadata["model_version"]}


@app.get("/v1/model")
def model():
    return {key: service.metadata[key] for key in ("model_name", "model_version", "metrics", "sha256")}


@app.post("/v1/predict")
def predict(payload: PredictionRequest):
    started = time.perf_counter()
    trace_id = str(uuid.uuid4())
    try:
        result = service.predict(Transaction(**payload.model_dump()))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    REQUESTS.labels(result["decision"]).inc()
    LATENCY.observe(time.perf_counter() - started)
    return result | {"trace_id": trace_id, "environment": os.getenv("ENVIRONMENT", "local")}
