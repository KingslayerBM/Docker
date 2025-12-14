from fastapi import APIRouter, HTTPException
from adapters.http.schemas import CreateOrderRequest, CreateOrderResponse, OrderResponse
from core.domain.errors import ValidationError
from core.usecases.create_order import CreateOrder, CreateOrderCommand
from core.usecases.get_order import GetOrder

def build_router(create_uc: CreateOrder, get_uc: GetOrder) -> APIRouter:
    router = APIRouter()

    @router.post("/orders", status_code=201, response_model=CreateOrderResponse)
    def create_order(req: CreateOrderRequest):
        try:
            oid = create_uc.execute(CreateOrderCommand(sku=req.sku, qty=req.qty))
            return CreateOrderResponse(id=oid)
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=str(e))

    @router.get("/orders/{order_id}", response_model=OrderResponse)
    def get_order(order_id: str):
        order = get_uc.execute(order_id)
        if order is None:
            raise HTTPException(status_code=404, detail="order not found")
        return OrderResponse(id=order.id, sku=order.sku, qty=order.qty)

    return router
