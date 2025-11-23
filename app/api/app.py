from fastapi import FastAPI

from app.api.articles.router import router as articles_router
from app.api.auth.router import router as auth_router
from app.api.deposits.router import router as deposits_router
from app.api.handlers import add_exception_handler
from app.api.inventories.router import router as inventories_router
from app.api.items.router import router as items_router
from app.api.price_labels.router import router as tags_router
from app.api.producers.router import router as producers_router
from app.api.utils import add_session_middleware, mount_static
from app.api.volumes.router import router as volumes_router
from app.core.config import Settings


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        title=settings.project_name,
        version=settings.app_version,
    )

    add_session_middleware(app=app, settings=settings)
    add_exception_handler(app=app, settings=settings)
    mount_static(app=app, settings=settings)

    app.include_router(auth_router)
    app.include_router(articles_router)
    app.include_router(producers_router)
    app.include_router(items_router)
    app.include_router(volumes_router)
    app.include_router(deposits_router)
    app.include_router(tags_router)
    app.include_router(inventories_router)

    return app
