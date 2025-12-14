import os, time, requests

BASE = os.environ.get("GATEWAY_BASE", "http://localhost:8080")

def wait_up(timeout=60):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(BASE + "/health", timeout=2)
            if r.status_code == 200:
                return
        except Exception:
            pass
        time.sleep(1)
    raise RuntimeError("Gateway did not become healthy")

def test_e2e_through_gateway():
    wait_up()

    r = requests.get(BASE + "/catalog/items", timeout=5)
    assert r.status_code == 200
    items = r.json()
    assert isinstance(items, list) and len(items) >= 1

    payload = {"userId": 1, "itemId": items[0]["id"], "qty": 1}
    r = requests.post(BASE + "/orders", json=payload, timeout=5)
    assert r.status_code == 201
    oid = r.json()["id"]

    r = requests.get(BASE + f"/orders/{oid}", timeout=5)
    assert r.status_code == 200
    order = r.json()
    assert order["id"] == oid
    assert order["qty"] == 1
