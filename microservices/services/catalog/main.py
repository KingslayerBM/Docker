from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="Catalog Service", version="1.0.0")

ITEMS = [
    {"id": 1, "name": "Desk"},
    {"id": 2, "name": "Chair"},
]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/items")
def list_items():
    return JSONResponse(content=ITEMS)
