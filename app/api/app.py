from fastapi import FastAPI

from app.api.articles.router import router as articles_router
from app.api.auth.router import router as auth_router
from app.api.categories.router import router as categories_router
from app.api.deposits.router import router as deposits_router
from app.api.distributors.router import router as distributors_router
from app.api.handlers import add_exception_handler
from app.api.inventories.router import router as inventories_router
from app.api.origins.router import router as origins_router
from app.api.price_labels.router import router as tags_router
from app.api.producers.router import router as producers_router
from app.api.stores.router import router as stores_router
from app.api.utils import add_security_middleware, add_session_middleware, mount_static
from app.api.volumes.router import router as volumes_router
from app.core.config.settings import Settings


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        title=settings.project_name,
        version=settings.app_version,
    )

    add_session_middleware(app=app, settings=settings)
    add_security_middleware(app=app, settings=settings)

    add_exception_handler(app=app, settings=settings)
    mount_static(app=app, settings=settings)

    app.include_router(auth_router)
    app.include_router(stores_router)
    app.include_router(categories_router)
    app.include_router(articles_router)
    app.include_router(producers_router)
    app.include_router(distributors_router)
    app.include_router(origins_router)
    app.include_router(volumes_router)
    app.include_router(deposits_router)
    app.include_router(tags_router)
    app.include_router(inventories_router)

    return app
