from decimal import Decimal
from pydantic import BaseModel
from enum import Enum


class ProductCreate(BaseModel):
    name: str
    description: str
    price: Decimal


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: Decimal
    views_count: int

    class Config:
        from_attributes = True


class ProductSorting(str, Enum):
    name_asc = "name"  # A-Z
    name_desc = "-name"  # Z-A
    price_desc = "price"
    price_asc = "-price"
    views_asc = "-views_count"
