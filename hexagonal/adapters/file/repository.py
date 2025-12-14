from __future__ import annotations
from typing import Optional
import csv
import os
from core.domain.order import Order
from core.ports.order_repository import OrderRepository, OrderId

class CsvOrderRepository(OrderRepository):
    """CSV format: id,sku,qty"""
    def __init__(self, csv_path: str):
        self._path = csv_path
        os.makedirs(os.path.dirname(self._path) or ".", exist_ok=True)
        if not os.path.exists(self._path):
            with open(self._path, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(["id", "sku", "qty"])

    def create(self, order: Order) -> OrderId:
        with open(self._path, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([order.id, order.sku, str(order.qty)])
        return order.id

    def get_by_id(self, order_id: OrderId) -> Optional[Order]:
        if not os.path.exists(self._path):
            return None
        with open(self._path, "r", newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("id") == order_id:
                    return Order(id=row["id"], sku=row["sku"], qty=int(row["qty"]))
        return None
