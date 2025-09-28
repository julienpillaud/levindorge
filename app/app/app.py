from cleanstack.fastapi.exceptions import add_exception_handler
from fastapi import FastAPI

from app.app.articles.router import router as articles_router
from app.app.auth.router import router as auth_router
from app.app.price_labels.router import router as tags_router
from app.app.utils import add_session_middleware, mount_static
from app.core.config import Settings


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        title=settings.project_name,
        version=settings.api_version,
    )

    add_session_middleware(app=app, settings=settings)
    add_exception_handler(app=app)
    mount_static(app=app, settings=settings)

    app.include_router(auth_router)
    app.include_router(articles_router)
    app.include_router(tags_router)

    return app
