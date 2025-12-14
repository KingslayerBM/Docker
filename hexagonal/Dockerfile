# syntax=docker/dockerfile:1
FROM python:3.11-slim AS builder
WORKDIR /build
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_NO_CACHE_DIR=1
COPY requirements.txt .
RUN pip wheel --wheel-dir /wheels -r requirements.txt

FROM python:3.11-slim AS runtime
WORKDIR /app
ENV PYTHONUNBUFFERED=1
RUN useradd -m -u 10001 appuser
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels
COPY . /app
RUN chown -R appuser:appuser /app
USER appuser
EXPOSE 8081
HEALTHCHECK --interval=10s --timeout=2s --retries=12 CMD python -c "import urllib.request,os; urllib.request.urlopen(f'http://127.0.0.1:{os.getenv("PORT","8081")}/health', timeout=2).read()"
CMD ["python","-m","uvicorn","main:app","--host","0.0.0.0","--port","8081"]
