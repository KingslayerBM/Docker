from __future__ import annotations
from typing import Optional
import psycopg
from core.domain.order import Order
from core.ports.order_repository import OrderRepository, OrderId
from .db import DbConfig

class PostgresOrderRepository(OrderRepository):
    def __init__(self, cfg: DbConfig):
        self._cfg = cfg

    def create(self, order: Order) -> OrderId:
        with psycopg.connect(self._cfg.dsn) as conn:
            conn.execute("INSERT INTO orders(id, sku, qty) VALUES (%s, %s, %s);", (order.id, order.sku, order.qty))
            conn.commit()
        return order.id

    def get_by_id(self, order_id: OrderId) -> Optional[Order]:
        with psycopg.connect(self._cfg.dsn) as conn:
            row = conn.execute("SELECT id, sku, qty FROM orders WHERE id=%s;", (order_id,)).fetchone()
            if not row:
                return None
            oid, sku, qty = row
            return Order(id=str(oid), sku=str(sku), qty=int(qty))
