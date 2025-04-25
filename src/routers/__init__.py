from routers.users_router import users_router
from routers.products_router import products_router


def include_routes(app):
    app.include_router(products_router)
    app.include_router(users_router)
