from pydantic import BaseModel, Field

class CreateOrderRequest(BaseModel):
    sku: str = Field(min_length=1, max_length=100)
    qty: int = Field(gt=0)

class CreateOrderResponse(BaseModel):
    id: str

class OrderResponse(BaseModel):
    id: str
    sku: str
    qty: int
