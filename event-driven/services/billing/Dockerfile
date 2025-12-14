FROM python:3.11-slim

WORKDIR /app

RUN adduser --disabled-password appuser \
    && mkdir -p /data \
    && chown -R appuser:appuser /data

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

USER appuser

CMD ["python", "main.py"]