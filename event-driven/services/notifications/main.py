import json
import os
import time
import uuid
from datetime import datetime, timezone

from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable


BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "orders.events")
GROUP_ID = os.getenv("KAFKA_GROUP_ID", "notifications")


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def wait_for_kafka(create_fn, retries=30, delay=2):
    for i in range(retries):
        try:
            return create_fn()
        except NoBrokersAvailable:
            print(f"[notifications] Kafka not ready {i+1}/{retries}")
            time.sleep(delay)
    raise RuntimeError("Kafka not available")


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

print("[notifications] started", flush=True)

for msg in consumer:
    event = msg.value

    if event.get("type") != "PaymentCaptured":
        continue

    oid = event["orderId"]

    email = {
        "type": "EmailSent",
        "eventId": str(uuid.uuid4()),
        "orderId": oid,
        "to": "user@example.com",
        "ts": utc_now(),
    }

    print(f"[notifications] Email sent for {oid}", flush=True)
    producer.send(TOPIC, key=oid, value=email)
    producer.flush()