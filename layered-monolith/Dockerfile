# syntax=docker/dockerfile:1

FROM python:3.12-slim AS builder

WORKDIR /build

# Install build tools (kept minimal)
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY app ./app

# --- runtime image ---
FROM python:3.12-slim AS runtime

# curl is used by container HEALTHCHECK
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# non-root user
RUN useradd -m -u 10001 appuser

WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /build/app ./app

ENV PATH="/opt/venv/bin:$PATH"
ENV PORT=8080

EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=3s --retries=5 CMD curl -fsS http://localhost:${PORT}/health || exit 1

USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
