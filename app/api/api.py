from cleanstack.fastapi.exceptions import add_exception_handler
from fastapi import FastAPI

from app.api.articles.router import router as articles_router
from app.api.auth.router import router as auth_router
from app.core.config import Settings


def create_api(settings: Settings) -> FastAPI:
    app = FastAPI(
        title=settings.project_name,
        version=settings.api_version,
        swagger_ui_parameters={
            "tryItOutEnabled": True,
            "displayRequestDuration": True,
            "persistAuthorization": True,
        },
    )

    add_exception_handler(app=app)

    app.include_router(auth_router)
    app.include_router(articles_router)

    return app
