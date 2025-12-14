from __future__ import annotations

from fastapi import Depends, Request

from app.application.contracts import ProductRepository
from app.application.create_product import CreateProduct
from app.application.list_products import ListProducts


def get_repo(request: Request) -> ProductRepository:
    # repo_factory is defined in the composition root (app.main)
    return request.app.state.repo_factory()


def get_create_product_uc(repo: ProductRepository = Depends(get_repo)) -> CreateProduct:
    return CreateProduct(repo)


def get_list_products_uc(repo: ProductRepository = Depends(get_repo)) -> ListProducts:
    return ListProducts(repo)
