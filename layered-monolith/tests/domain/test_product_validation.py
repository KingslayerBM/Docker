import pytest
from decimal import Decimal

from app.domain.errors import ValidationError
from app.domain.product import Product


def test_product_rejects_empty_name():
    with pytest.raises(ValidationError):
        Product.new(name="   ", price=Decimal("10"))


def test_product_rejects_negative_price():
    with pytest.raises(ValidationError):
        Product.new(name="Desk", price=Decimal("-1"))


def test_product_accepts_valid_data():
    p = Product.new(name="Desk", price=Decimal("199.9"))
    assert p.id is None
    assert p.name == "Desk"
