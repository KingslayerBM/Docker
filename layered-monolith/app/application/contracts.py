from __future__ import annotations

from typing import Protocol, Sequence

from app.domain.product import Product


class ProductRepository(Protocol):
    def create(self, product: Product) -> int:
        """Persist product and return generated id."""

    def list(self) -> Sequence[Product]:
        """Return all products ordered by id asc."""
