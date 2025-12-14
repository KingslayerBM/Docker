import pytest
from core.domain.order import new_order
from core.domain.errors import ValidationError

def test_qty_must_be_positive():
    with pytest.raises(ValidationError):
        new_order("id1", "ABC", 0)
    with pytest.raises(ValidationError):
        new_order("id1", "ABC", -1)

def test_sku_must_not_be_empty():
    with pytest.raises(ValidationError):
        new_order("id1", "", 1)
    with pytest.raises(ValidationError):
        new_order("id1", "   ", 1)
