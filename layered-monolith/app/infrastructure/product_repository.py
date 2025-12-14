from __future__ import annotations

import json
from decimal import Decimal
from typing import Sequence, Any

from app.application.contracts import ProductRepository
from app.domain.product import Product


class PostgresProductRepository(ProductRepository):
    def __init__(self, pool: Any):
        self._pool = pool

    def create(self, product: Product) -> int:
        with self._pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO products (name, price) VALUES (%s, %s) RETURNING id",
                    (product.name, product.price),
                )
                new_id = cur.fetchone()[0]
            conn.commit()
        return int(new_id)

    def list(self) -> Sequence[Product]:
        with self._pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, price FROM products ORDER BY id ASC")
                rows = cur.fetchall()
        return [Product(id=int(r[0]), name=str(r[1]), price=Decimal(r[2])) for r in rows]


class CachedProductRepository(ProductRepository):
    """Redis cache wrapper for list() with TTL=30s."""

    CACHE_KEY = "products:list"
    TTL_SECONDS = 30

    def __init__(self, inner: ProductRepository, redis_client: Any):
        self._inner = inner
        self._redis = redis_client  # may be None

    def create(self, product: Product) -> int:
        new_id = self._inner.create(product)
        if self._redis is not None:
            try:
                self._redis.delete(self.CACHE_KEY)
            except Exception:
                pass
        return new_id

    def list(self) -> Sequence[Product]:
        if self._redis is not None:
            try:
                cached = self._redis.get(self.CACHE_KEY)
                if cached:
                    payload = json.loads(cached.decode("utf-8"))
                    return [
                        Product(
                            id=int(p["id"]),
                            name=str(p["name"]),
                            price=Decimal(str(p["price"])),
                        )
                        for p in payload
                    ]
            except Exception:
                pass

        products = list(self._inner.list())

        if self._redis is not None:
            try:
                payload = [{"id": p.id, "name": p.name, "price": str(p.price)} for p in products]
                self._redis.setex(self.CACHE_KEY, self.TTL_SECONDS, json.dumps(payload).encode("utf-8"))
            except Exception:
                pass

        return products
