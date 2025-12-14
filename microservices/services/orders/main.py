from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
import uuid

app = FastAPI(title="Orders Service", version="1.0.0")

class CreateOrderRequest(BaseModel):
    userId: int
    itemId: int
    qty: int = Field(gt=0)

ORDERS: dict[str, dict] = {}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/orders", status_code=201)
def create_order(req: CreateOrderRequest):
    oid = str(uuid.uuid4())
    order = {"id": oid, "userId": req.userId, "itemId": req.itemId, "qty": req.qty}
    ORDERS[oid] = order
    return JSONResponse(content={"id": oid}, status_code=201)

@app.get("/orders/{order_id}")
def get_order(order_id: str):
    order = ORDERS.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return JSONResponse(content=order)
