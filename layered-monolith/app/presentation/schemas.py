from __future__ import annotations

from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict


class CreateProductRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: Decimal = Field(gt=0)

    model_config = ConfigDict(extra="forbid")


class CreateProductResponse(BaseModel):
    id: int


class ProductResponse(BaseModel):
    id: int
    name: str
    price: Decimal

    model_config = ConfigDict(json_encoders={Decimal: float})


class HealthResponse(BaseModel):
    status: str
