from decimal import Decimal

from injector import Inject
from pydantic import BaseModel, Field
from pydiator_core.interfaces import BaseHandler, BaseRequest, BaseResponse

from app.exceptions import EntityNotExistsException
from repositories.product_repository import ProductRepository
from schemas.products import ProductResponse


class GetProductRequest(BaseModel, BaseRequest):
    id: int = Field(gt=0)


class GetProductResponse(BaseModel, BaseResponse):
    product: ProductResponse


class GetProductHandler(BaseHandler):
    def __init__(self, product_repository: Inject[ProductRepository]):
        self._product_repository = product_repository

    async def handle(self, req: GetProductRequest) -> GetProductResponse:  # type: ignore
        product = await self._product_repository.get_by_id(product_id=req.id)
        if not product:
            raise EntityNotExistsException(f"Product with ID={req.id} does not exist!")
        views_count = product.views_count
        product.views_count = views_count + 1
        product = await self._product_repository.update_product(product=product)
        return GetProductResponse(product=ProductResponse.from_orm(product))
