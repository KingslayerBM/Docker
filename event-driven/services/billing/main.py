import json
import os
import sqlite3
import time
import uuid
from datetime import datetime, timezone

from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable


BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "orders.events")
GROUP_ID = os.getenv("KAFKA_GROUP_ID", "billing")
DB_PATH = "/data/billing.db"


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def wait_for_kafka(create_fn, retries=30, delay=2):
    for i in range(retries):
        try:
            return create_fn()
        except NoBrokersAvailable:
            print(f"[billing] Kafka not ready {i+1}/{retries}")
            time.sleep(delay)
    raise RuntimeError("Kafka not available")


# ---- SQLite init (idempotency storage) ----
os.makedirs("/data", exist_ok=True)
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
conn.execute(
    "CREATE TABLE IF NOT EXISTS processed_events (event_id TEXT PRIMARY KEY)"
)
conn.commit()


def processed(event_id: str) -> bool:
    cur = conn.execute("SELECT 1 FROM processed_events WHERE event_id=?", (event_id,))
    return cur.fetchone() is not None


def mark(event_id: str):
    conn.execute("INSERT OR IGNORE INTO processed_events VALUES (?)", (event_id,))
    conn.commit()


# ---- Kafka ----
consumer = wait_for_kafka(
    lambda: KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP,
        group_id=GROUP_ID,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda b: json.loads(b.decode()),
    )
)

producer = wait_for_kafka(
    lambda: KafkaProducer(
        bootstrap_servers=BOOTSTRAP,
        value_serializer=lambda v: json.dumps(v).encode(),
        key_serializer=lambda v: v.encode(),
    )
)

print("[billing] started", flush=True)


# ---- Event loop ----
for msg in consumer:
    event = msg.value

    if event.get("type") != "OrderCreated":
        continue

    eid = event["eventId"]
    oid = event["orderId"]

    if processed(eid):
        print(f"[billing] duplicate ignored {eid}", flush=True)
        continue

    amount = event["qty"] * 100
    mark(eid)

    payment = {
        "type": "PaymentCaptured",
        "eventId": str(uuid.uuid4()),
        "orderId": oid,
        "amount": amount,
        "ts": utc_now(),
    }

    producer.send(TOPIC, key=oid, value=payment)
    producer.flush()

    print(f"[billing] PaymentCaptured {oid}", flush=True)