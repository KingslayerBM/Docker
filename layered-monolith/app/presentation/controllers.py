from __future__ import annotations

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.application.dto import CreateProductDTO
from app.domain.errors import ValidationError
from app.presentation.dependencies import get_create_product_uc, get_list_products_uc
from app.presentation.schemas import (
    CreateProductRequest,
    CreateProductResponse,
    ProductResponse,
    HealthResponse,
)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/products", response_model=list[ProductResponse])
def list_products(uc=Depends(get_list_products_uc)) -> list[ProductResponse]:
    products = uc.execute()
    return [ProductResponse(id=p.id, name=p.name, price=p.price) for p in products]


@router.post(
    "/products",
    response_model=CreateProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(req: CreateProductRequest, uc=Depends(get_create_product_uc)) -> CreateProductResponse:
    try:
        dto = CreateProductDTO(name=req.name, price=req.price)
        new_id = uc.execute(dto)
        return CreateProductResponse(id=new_id)
    except ValidationError as e:
        return JSONResponse(status_code=400, content={"detail": str(e)})
