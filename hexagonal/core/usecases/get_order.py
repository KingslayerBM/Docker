from __future__ import annotations
from typing import Optional
from core.domain.order import Order
from core.ports.order_repository import OrderRepository, OrderId

class GetOrder:
    def __init__(self, repo: OrderRepository):
        self._repo = repo

    def execute(self, order_id: OrderId) -> Optional[Order]:
        return self._repo.get_by_id(order_id)
