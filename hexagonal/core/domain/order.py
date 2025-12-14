from dataclasses import dataclass
from .errors import ValidationError

@dataclass(frozen=True)
class Order:
    id: str
    sku: str
    qty: int

def validate_sku(sku: str) -> None:
    if sku is None or not str(sku).strip():
        raise ValidationError("sku must not be empty")
    if len(str(sku).strip()) > 100:
        raise ValidationError("sku length must be <= 100")

def validate_qty(qty: int) -> None:
    try:
        q = int(qty)
    except Exception:
        raise ValidationError("qty must be an integer")
    if q <= 0:
        raise ValidationError("qty must be > 0")

def new_order(order_id: str, sku: str, qty: int) -> Order:
    validate_sku(sku)
    validate_qty(qty)
    return Order(id=order_id, sku=str(sku).strip(), qty=int(qty))
