import json
import os
import time
import uuid
from datetime import datetime, timezone

from fastapi import FastAPI
from pydantic import BaseModel
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable


BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "orders.events")

app = FastAPI()


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def wait_for_kafka(create_fn, retries=30, delay=2):
    for i in range(retries):
        try:
            return create_fn()
        except NoBrokersAvailable:
            print(f"[orders] Kafka not ready {i+1}/{retries}")
            time.sleep(delay)
    raise RuntimeError("Kafka not available")


producer = None


@app.on_event("startup")
def startup():
    global producer
    producer = wait_for_kafka(
        lambda: KafkaProducer(
            bootstrap_servers=BOOTSTRAP,
            value_serializer=lambda v: json.dumps(v).encode(),
            key_serializer=lambda v: v.encode(),
        )
    )
    print("[orders] Kafka producer ready", flush=True)


class OrderIn(BaseModel):
    userId: int
    itemId: int
    qty: int


@app.post("/orders")
def create_order(data: OrderIn):
    order_id = str(uuid.uuid4())

    event = {
        "type": "OrderCreated",
        "eventId": str(uuid.uuid4()),
        "orderId": order_id,
        "userId": data.userId,
        "itemId": data.itemId,
        "qty": data.qty,
        "ts": utc_now(),
    }

    producer.send(TOPIC, key=order_id, value=event)
    producer.flush()

    return {"orderId": order_id}
