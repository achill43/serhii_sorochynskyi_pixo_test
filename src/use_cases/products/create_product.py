from decimal import Decimal

from injector import Inject
from pydantic import BaseModel, model_validator
from pydiator_core.interfaces import BaseHandler, BaseRequest, BaseResponse

from app.exceptions import ValidationError
from config import Settings
from models.products import ProductSQL
from repositories.product_repository import ProductRepository
from schemas.products import ProductResponse


class CreateProductRequest(BaseModel, BaseRequest):
    name: str
    description: str
    price: Decimal

    @model_validator(mode="before")
    @classmethod
    def price_validation(cls, values: dict) -> dict:
        if values.get("price", 0.0) <= 0:
            raise ValidationError("Price must be more than 0!")
        return values


class CreateProductResponse(BaseModel, BaseResponse):
    product: ProductResponse


class CreateProductHandler(BaseHandler):
    def __init__(
        self, product_repository: Inject[ProductRepository], settings: Inject[Settings]
    ):
        self._product_repository = product_repository
        self._settings = settings

    async def handle(self, req: CreateProductRequest) -> CreateProductResponse:  # type: ignore
        product_item = req.dict()
        product_item["views_count"] = 0
        product = await self._product_repository.create_product(
            ProductSQL(**product_item)
        )
        return CreateProductResponse(product=ProductResponse.from_orm(product))
