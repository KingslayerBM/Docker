from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from .errors import ValidationError


def validate_name(name: str) -> str:
    if name is None:
        raise ValidationError("name is required")
    name = name.strip()
    if len(name) < 1:
        raise ValidationError("name must not be empty")
    if len(name) > 100:
        raise ValidationError("name must be at most 100 characters")
    return name


def validate_price(price: Decimal) -> Decimal:
    if price is None:
        raise ValidationError("price is required")
    if price <= Decimal("0"):
        raise ValidationError("price must be greater than 0")
    return price


@dataclass(frozen=True, slots=True)
class Product:
    """Domain entity."""
    id: int | None
    name: str
    price: Decimal

    @staticmethod
    def new(name: str, price: Decimal) -> "Product":
        return Product(id=None, name=validate_name(name), price=validate_price(price))

    def with_id(self, new_id: int) -> "Product":
        if new_id is None or new_id <= 0:
            raise ValidationError("id must be a positive integer")
        return Product(id=new_id, name=self.name, price=self.price)
