from __future__ import annotations
from dataclasses import dataclass
from uuid import uuid4

from core.domain.order import new_order
from core.ports.order_repository import OrderRepository, OrderId

@dataclass(frozen=True)
class CreateOrderCommand:
    sku: str
    qty: int

class CreateOrder:
    def __init__(self, repo: OrderRepository):
        self._repo = repo

    def execute(self, cmd: CreateOrderCommand) -> OrderId:
        order_id = str(uuid4())
        order = new_order(order_id=order_id, sku=cmd.sku, qty=cmd.qty)
        return self._repo.create(order)
