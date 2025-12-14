from __future__ import annotations

from app.application.contracts import ProductRepository
from app.application.dto import CreateProductDTO
from app.domain.product import Product


class CreateProduct:
    def __init__(self, repo: ProductRepository):
        self._repo = repo

    def execute(self, dto: CreateProductDTO) -> int:
        product = Product.new(name=dto.name, price=dto.price)
        return self._repo.create(product)
