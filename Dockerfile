FROM python:3.11-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=8000
WORKDIR /app
COPY --from=builder /install /usr/local
COPY src ./src
RUN python -m src.platform_api.train
RUN useradd --uid 10001 --no-create-home appuser && chown -R appuser:appuser /app
USER 10001
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/live')"
CMD ["uvicorn", "src.platform_api.api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
