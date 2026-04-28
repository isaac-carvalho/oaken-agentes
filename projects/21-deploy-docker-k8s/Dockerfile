# syntax=docker/dockerfile:1.6
FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.12-slim AS runtime
RUN useradd -m -u 1000 oaken
WORKDIR /app
COPY --from=builder /root/.local /home/oaken/.local
COPY app.py ./
COPY _shared ./_shared
ENV PATH=/home/oaken/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app
USER oaken
EXPOSE 8000

# Resource hints for container orchestrators (enforced by k8s limits, not Docker itself)
LABEL oaken.resources.cpu="0.5" \
      oaken.resources.memory="256Mi" \
      oaken.resources.memory-limit="512Mi"

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request, json; r=urllib.request.urlopen('http://localhost:8000/health'); d=json.loads(r.read()); assert d.get('status')=='ok', f'unhealthy: {d}'"
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--limit-max-requests", "10000"]
