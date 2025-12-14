from typing import Optional, Dict
import pytest
from core.domain.order import Order
from core.usecases.create_order import CreateOrder, CreateOrderCommand
from core.usecases.get_order import GetOrder
from core.domain.errors import ValidationError

class FakeRepo:
    def __init__(self):
        self.store: Dict[str, Order] = {}

    def create(self, order: Order) -> str:
        self.store[order.id] = order
        return order.id

    def get_by_id(self, order_id: str) -> Optional[Order]:
        return self.store.get(order_id)

def test_create_and_get_order_happy_path():
    repo = FakeRepo()
    create_uc = CreateOrder(repo)
    get_uc = GetOrder(repo)
    oid = create_uc.execute(CreateOrderCommand(sku="ABC", qty=2))
    got = get_uc.execute(oid)
    assert got is not None
    assert got.id == oid
    assert got.sku == "ABC"
    assert got.qty == 2

def test_create_raises_on_invalid_input():
    repo = FakeRepo()
    create_uc = CreateOrder(repo)
    with pytest.raises(ValidationError):
        create_uc.execute(CreateOrderCommand(sku="", qty=2))
    with pytest.raises(ValidationError):
        create_uc.execute(CreateOrderCommand(sku="ABC", qty=0))
