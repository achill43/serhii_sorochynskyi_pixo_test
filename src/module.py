import injector
from fastapi_injector import request_scope
from sqlalchemy.ext.asyncio.session import AsyncSession
from request_context import RequestContextProvider

from config import Settings, settings
from db import SessionLocal
from repositories.user_repository import UserRepository
from repositories.product_repository import ProductRepository


def configure_for_production(binder: injector.Binder) -> None:
    binder.bind(Settings, to=settings)


class CoreModule(injector.Module):
    @injector.provider
    @request_scope
    def get_request_context(self) -> RequestContextProvider:
        return RequestContextProvider()

    @injector.provider
    @request_scope
    def get_session(self) -> AsyncSession:
        return SessionLocal()

    @injector.provider
    @request_scope
    def get_user_repo(self, session: AsyncSession) -> UserRepository:
        return UserRepository(session)

    @injector.provider
    @request_scope
    def get_product_repo(self, session: AsyncSession) -> ProductRepository:
        return ProductRepository(session)
