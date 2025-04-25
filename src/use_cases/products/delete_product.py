from decimal import Decimal

from injector import Inject
from pydantic import BaseModel, Field
from pydiator_core.interfaces import BaseHandler, BaseRequest, BaseResponse

from app.exceptions import EntityNotExistsException
from repositories.product_repository import ProductRepository


class DeleteProductRequest(BaseModel, BaseRequest):
    id: int = Field(gt=0)


class DeleteProductResponse(BaseModel, BaseResponse):
    message: str


class DeleteProductHandler(BaseHandler):
    def __init__(self, product_repository: Inject[ProductRepository]):
        self._product_repository = product_repository

    async def handle(self, req: DeleteProductRequest) -> DeleteProductResponse:  # type: ignore
        product = await self._product_repository.get_by_id(product_id=req.id)
        if not product:
            raise EntityNotExistsException(f"Product with ID={req.id} does not exist!")
        product = await self._product_repository.delete_by_id(_id=req.id)
        return DeleteProductResponse(message="Product was deleted")
