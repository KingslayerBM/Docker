from __future__ import annotations
from typing import Protocol, Optional
from core.domain.order import Order

OrderId = str

class OrderRepository(Protocol):
    def create(self, order: Order) -> OrderId: ...
    def get_by_id(self, order_id: OrderId) -> Optional[Order]: ...
