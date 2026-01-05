import logging

from cleanstack.exceptions import ConflictError
from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse, RedirectResponse, Response
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.dependencies import get_templates
from app.core.config.settings import Settings
from app.domain.exceptions import (
    AlreadyExistsError,
    EntityInUseError,
    UserUnauthorizedError,
)

logger = logging.getLogger(__name__)


def add_exception_handler(app: FastAPI, settings: Settings) -> None:
    templates = get_templates(settings=settings)

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request, _: StarletteHTTPException
    ) -> Response:
        # TODO: implement error pages (404.html, ...)
        return RedirectResponse(
            url=request.url_for("home"),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    # @app.exception_handler(DomainError)
    # async def generic_handler(request: Request, _: Exception) -> Response:
    #     return templates.TemplateResponse(
    #         request=request,
    #         name="errors/error.html",
    #     )

    @app.exception_handler(UserUnauthorizedError)
    async def user_not_authorized_handler(request: Request, _: Exception) -> Response:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
        )

    @app.exception_handler(ConflictError)
    async def conflict_error_handler(request: Request, exc: ConflictError) -> Response:
        if isinstance(exc, AlreadyExistsError):
            message = f"'{exc.display_name}' existe déjà"
        elif isinstance(exc, EntityInUseError):
            message = f"'{exc.display_name}' ne peut pas être supprimé"
        else:
            message = "Conflit"

        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": message},
        )
