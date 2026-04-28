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
COPY ../_shared /app/projects/_shared
ENV PATH=/home/oaken/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app
USER oaken
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
