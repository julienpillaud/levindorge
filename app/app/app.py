from fastapi import FastAPI

from app.app.articles.router import router as articles_router
from app.app.auth.router import router as auth_router
from app.app.deposits.router import router as deposits_router
from app.app.handlers import add_exception_handler
from app.app.inventories.router import router as inventories_router
from app.app.items.router import router as items_router
from app.app.price_labels.router import router as tags_router
from app.app.utils import add_session_middleware, mount_static
from app.app.volumes.router import router as volumes_router
from app.core.config import Settings


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        title=settings.project_name,
        version=settings.api_version,
    )

    add_session_middleware(app=app, settings=settings)
    add_exception_handler(app=app, settings=settings)
    mount_static(app=app, settings=settings)

    app.include_router(auth_router)
    app.include_router(articles_router)
    app.include_router(items_router)
    app.include_router(volumes_router)
    app.include_router(deposits_router)
    app.include_router(tags_router)
    app.include_router(inventories_router)

    return app
