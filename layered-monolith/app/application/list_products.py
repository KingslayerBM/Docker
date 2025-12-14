from __future__ import annotations

from typing import Sequence

from app.application.contracts import ProductRepository
from app.domain.product import Product


class ListProducts:
    def __init__(self, repo: ProductRepository):
        self._repo = repo

    def execute(self) -> Sequence[Product]:
        return self._repo.list()
