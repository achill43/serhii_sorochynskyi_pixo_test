from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_injector import InjectorMiddleware, attach_injector

from config import settings
from app.exceptions import (
    EntityAlreadyExistsException,
    ValidationError,
    EntityNotExistsException,
)
from app.exception_handles import ExceptionHandlers
from injector_setup import injector_setup
from pydiator_setup import setup_pydiator
from routers import include_routes


def init_app():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """
        Function that handles startup and shutdown events.
        To understand more, read https://fastapi.tiangolo.com/advanced/events/
        """
        yield

    # Ініціалізація застосунку FastAPI
    _app = FastAPI(title=settings.PROJECT_NAME, docs_url="/api/docs")

    injector = injector_setup(app=_app)
    attach_injector(_app, injector)
    setup_pydiator(injector)

    # Exception handler
    _app.add_exception_handler(Exception, ExceptionHandlers.unhandled_exception)
    _app.add_exception_handler(EntityNotExistsException, ExceptionHandlers.not_exists)
    _app.add_exception_handler(
        EntityAlreadyExistsException, ExceptionHandlers.already_exists
    )
    _app.add_exception_handler(
        ValidationError, ExceptionHandlers.internal_validation_exception
    )

    # Middlewares
    _app.add_middleware(InjectorMiddleware, injector=injector)
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    include_routes(_app)

    return _app


app = init_app()
