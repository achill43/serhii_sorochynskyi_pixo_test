from decimal import Decimal

from sqlalchemy import String, Integer, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class ProductSQL(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True, unique=True
    )
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column()
    price: Mapped[Decimal] = mapped_column(DECIMAL(20, 2))
    views_count: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return f"<Product id={self.id} name={self.name}>"

    def __str__(self) -> str:
        return self.__repr__()
