from typing import cast, Tuple, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, delete, desc

from models.products import ProductSQL
from schemas.products import ProductSorting


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_product(self, user: ProductSQL) -> ProductSQL:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_by_id(self, product_id: int) -> ProductSQL:
        result = await self.db.execute(select(ProductSQL).filter_by(id=product_id))
        return result.scalar_one_or_none()

    async def update_product(self, product: ProductSQL) -> ProductSQL:
        await self.db.merge(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def delete_by_id(self, _id: int):
        product = cast(
            ProductSQL,
            await self.db.scalar(select(ProductSQL).where(ProductSQL.id == _id)),
        )
        if not product:
            return None
        await self.db.execute(delete(ProductSQL).where(ProductSQL.id == _id))
        await self.db.commit()

    async def get_paginated(
        self,
        page: int,
        page_size: int,
        sort: ProductSorting = ProductSorting.name_asc,
    ) -> Tuple[Sequence[ProductSQL], int]:
        query = select(ProductSQL)

        # Apply sorting
        sort_attr = sort.value.lstrip("-")
        sort_column = getattr(ProductSQL, sort_attr)
        if sort.value.startswith("-"):
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(sort_column)

        total: int = await self.db.scalar(
            select(func.count()).select_from(query)
        )  # type: ignore
        products = await self.db.scalars(
            query.offset((page - 1) * page_size).limit(page_size)
        )
        return products, total
