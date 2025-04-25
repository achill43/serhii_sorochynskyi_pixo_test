from decimal import Decimal
from typing import cast

import pytest
from app.exceptions import ValidationError
from sqlalchemy import select

from models.products import ProductSQL
from use_cases.products.create_product import (
    CreateProductRequest,
    CreateProductResponse,
)

DATABASE_URL = "sqlite+aiosqlite:///./test.db"


@pytest.mark.asyncio
async def test_creating_product(test_app, db_session):
    app, injector, pydiator = test_app
    response = cast(
        CreateProductResponse,
        await pydiator.send(
            req=CreateProductRequest(
                name="Product 1", description="Description 1", price=Decimal(5.5)
            )
        ),
    )
    product = await db_session.scalar(
        select(ProductSQL).where(ProductSQL.id == response.product.id)
    )
    assert product


@pytest.mark.asyncio
async def test_creating_product_wrong_price(test_app, db_session):
    app, injector, pydiator = test_app
    raise_error = False
    try:
        _ = cast(
            CreateProductResponse,
            await pydiator.send(
                req=CreateProductRequest(
                    name="Product 1", description="Description 1", price=Decimal(-5.5)
                )
            ),
        )
    except ValidationError:
        raise_error = True
    assert raise_error is True
