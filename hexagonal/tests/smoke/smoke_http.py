"""Smoke test runner for a running container.
ENV:
  BASE_URL (default http://localhost:8081)
"""
import os, json, time, urllib.request, urllib.error

BASE_URL = os.getenv("BASE_URL", "http://localhost:8081").rstrip("/")

def http(method: str, path: str, body=None, expect=200):
    url = BASE_URL + path
    data = None
    headers = {}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode("utf-8")
            if resp.status != expect:
                raise AssertionError(f"{method} {path}: expected {expect}, got {resp.status}: {raw}")
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8")
        if e.code != expect:
            raise AssertionError(f"{method} {path}: expected {expect}, got {e.code}: {raw}")
        return json.loads(raw) if raw else None

def main():
    for _ in range(30):
        try:
            http("GET", "/health", expect=200)
            break
        except Exception:
            time.sleep(1)
    created = http("POST", "/orders", {"sku":"ABC","qty":2}, expect=201)
    oid = created["id"]
    got = http("GET", f"/orders/{oid}", expect=200)
    assert got["id"] == oid and got["sku"] == "ABC" and got["qty"] == 2
    http("GET", "/orders/00000000-0000-0000-0000-000000000000", expect=404)
    print("SMOKE OK")

if __name__ == "__main__":
    main()
