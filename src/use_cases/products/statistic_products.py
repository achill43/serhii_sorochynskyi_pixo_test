from injector import Inject
from pydantic import BaseModel, Field
from pydiator_core.interfaces import BaseHandler, BaseRequest, BaseResponse

from repositories.product_repository import ProductRepository
from schemas.products import ProductResponse, ProductSorting


class StatisticProductsRequest(BaseModel, BaseRequest):
    product_count: int = Field(gt=0)


class StatisticProductsResponse(BaseModel, BaseResponse):
    products: list[ProductResponse]


class StatisticProductsHandler(BaseHandler):
    def __init__(self, product_repository: Inject[ProductRepository]):
        self._product_repository = product_repository

    async def handle(self, req: StatisticProductsRequest) -> StatisticProductsResponse:  # type: ignore
        products, _ = await self._product_repository.get_paginated(
            page=1, page_size=req.product_count, sort=ProductSorting.views_asc
        )
        return StatisticProductsResponse(
            products=[ProductResponse.from_orm(product) for product in products],
        )
