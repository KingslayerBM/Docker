import pytest
from decimal import Decimal

from app.application.create_product import CreateProduct
from app.application.dto import CreateProductDTO
from app.domain.errors import ValidationError


class MockRepo:
    def __init__(self):
        self.created = []

    def create(self, product):
        self.created.append(product)
        return 123

    def list(self):
        return []


def test_create_product_throws_on_invalid_input():
    uc = CreateProduct(MockRepo())
    with pytest.raises(ValidationError):
        uc.execute(CreateProductDTO(name="", price=Decimal("10")))


def test_create_product_calls_repo_and_returns_id():
    repo = MockRepo()
    uc = CreateProduct(repo)
    new_id = uc.execute(CreateProductDTO(name="Desk", price=Decimal("199.9")))
    assert new_id == 123
    assert len(repo.created) == 1
    assert repo.created[0].name == "Desk"
