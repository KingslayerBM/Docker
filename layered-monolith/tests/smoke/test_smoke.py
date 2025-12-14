import os
os.environ["TESTING"] = "1"

from fastapi.testclient import TestClient

from app.main import create_app
from app.domain.product import Product


class InMemoryRepo:
    def __init__(self):
        self._items = []
        self._next_id = 1

    def create(self, product: Product) -> int:
        pid = self._next_id
        self._next_id += 1
        self._items.append(product.with_id(pid))
        return pid

    def list(self):
        return list(self._items)


def test_smoke_health_and_products_flow():
    app = create_app()
    repo = InMemoryRepo()
    app.state.repo_factory = lambda: repo

    client = TestClient(app)

    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

    r = client.post("/products", json={"name": "Desk", "price": 199.9})
    assert r.status_code == 201
    new_id = r.json()["id"]
    assert isinstance(new_id, int)

    r = client.get("/products")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["id"] == new_id
    assert data[0]["name"] == "Desk"
