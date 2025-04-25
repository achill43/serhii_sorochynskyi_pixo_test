from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_injector import InjectorMiddleware, attach_injector
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.responses import JSONResponse

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


limiter = Limiter(key_func=get_remote_address)


def init_app():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """
        Function that handles startup and shutdown events.
        To understand more, read https://fastapi.tiangolo.com/advanced/events/
        """
        yield

    _app = FastAPI(title=settings.PROJECT_NAME, docs_url="/api/docs")
    _app.state.limiter = limiter

    injector = injector_setup(app=_app)
    attach_injector(_app, injector)
    setup_pydiator(injector)

    # Exception
    _app.add_exception_handler(
        RateLimitExceeded,
        lambda r, e: JSONResponse(
            status_code=429, content={"detail": "Rate limit exceeded"}
        ),
    )
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
    _app.add_middleware(SlowAPIMiddleware)
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


@app.get("/limited")
@limiter.limit("5/minute")
async def limited_endpoint(request: Request):
    return {"message": "You are within the rate limit"}
