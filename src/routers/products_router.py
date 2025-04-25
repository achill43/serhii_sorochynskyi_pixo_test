from depends.auth_deps import get_current_user
from fastapi import APIRouter, Depends, status
from pydiator_core.mediatr import pydiator
from schemas.users import UserResponse

from use_cases.products.create_product import (
    CreateProductRequest,
    CreateProductResponse,
)
from use_cases.products.get_one_product import GetProductRequest, GetProductResponse
from use_cases.products.get_product_list import (
    GetProductListRequest,
    GetProductListResponse,
)
from use_cases.products.delete_product import (
    DeleteProductRequest,
    DeleteProductResponse,
)
from use_cases.products.statistic_products import (
    StatisticProductsRequest,
    StatisticProductsResponse,
)


products_router = APIRouter(prefix="/products")


@products_router.post(
    "/",
    summary="Create new product",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": CreateProductResponse},
    },
)
async def create_product(
    req: CreateProductRequest, user: UserResponse = Depends(get_current_user)
):
    return await pydiator.send(req=req)


@products_router.get(
    "/{id}/",
    summary="Get one product",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": GetProductResponse},
    },
)
async def get_product(id: int):
    return await pydiator.send(req=GetProductRequest(id=id))


@products_router.get(
    "/",
    summary="Get products page",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": GetProductListResponse},
    },
)
async def get_product_list(
    req: GetProductListRequest = Depends(GetProductListRequest),
):
    return await pydiator.send(req=req)


@products_router.delete(
    "/{id}/",
    summary="Delete product",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": DeleteProductResponse},
    },
)
async def delete_product(
    req: DeleteProductRequest = Depends(DeleteProductRequest),
):
    return await pydiator.send(req=req)


@products_router.get(
    "/statistic",
    summary="Get most viewed products",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": StatisticProductsResponse},
    },
)
async def statistic_products(
    req: StatisticProductsRequest = Depends(StatisticProductsRequest),
):
    return await pydiator.send(req=req)
