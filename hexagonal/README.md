# Hexagonal (Ports & Adapters) — Orders API

Switch storage adapter **only by ENV**:

- `REPO_ADAPTER=db` → Postgres
- `REPO_ADAPTER=file` → CSV (`id,sku,qty`)

## Run

```bash
cp .env.example .env
docker compose up --build
```

API: http://localhost:8081

## Verify

```bash
curl -X POST localhost:8081/orders -H "Content-Type: application/json" -d '{"sku":"ABC","qty":2}'
curl localhost:8081/orders/<id>
```

## Switch to CSV

Edit `.env`:
```env
REPO_ADAPTER=file
CSV_PATH=/data/orders.csv
```

Data persists via `./data:/data`.

## Tests

```bash
docker compose run --rm api pytest -q
```

Optional smoke script against a running container:
```bash
python -m tests.smoke.smoke_http
```

## Architecture

- `core/` — entities, ports (interfaces), use-cases (no imports from adapters)
- `adapters/` — http, db, file implementations
- `config/` — ENV parsing + DI wiring
