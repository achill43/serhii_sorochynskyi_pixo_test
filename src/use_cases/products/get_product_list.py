from injector import Inject
from pydantic import BaseModel, Field
from pydiator_core.interfaces import BaseHandler, BaseRequest, BaseResponse

from repositories.product_repository import ProductRepository
from schemas.products import ProductResponse, ProductSorting


class GetProductListRequest(BaseModel, BaseRequest):
    page: int = Field(gt=0)
    page_size: int = Field(gt=1)
    sorting: ProductSorting


class GetProductListResponse(BaseModel, BaseResponse):
    total: int
    products: list[ProductResponse]


class GetProductListHandler(BaseHandler):
    def __init__(self, product_repository: Inject[ProductRepository]):
        self._product_repository = product_repository

    async def handle(self, req: GetProductListRequest) -> GetProductListResponse:  # type: ignore
        products, total = await self._product_repository.get_paginated(
            page=req.page, page_size=req.page_size, sort=req.sorting
        )
        return GetProductListResponse(
            total=total,
            products=[ProductResponse.from_orm(product) for product in products],
        )
