from cleanstack.exceptions import ConflictError, DomainError
from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException as StarletteHTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response

from app.app.dependencies import get_templates
from app.core.config import Settings
from app.domain.exceptions import (
    CannotDeleteError,
    UserUnauthorizedError,
)


def add_exception_handler(app: FastAPI, settings: Settings) -> None:
    templates = get_templates(settings=settings)

    @app.exception_handler(DomainError)
    @app.exception_handler(StarletteHTTPException)
    async def generic_handler(request: Request, _: Exception) -> Response:
        return templates.TemplateResponse(
            request=request,
            name="errors/error.html",
        )

    @app.exception_handler(UserUnauthorizedError)
    async def user_not_authorized_handler(request: Request, _: Exception) -> Response:
        return templates.TemplateResponse(
            request=request,
            name="errors/401.html",
        )

    @app.exception_handler(ConflictError)
    async def conflict_error_handler(request: Request, exc: ConflictError) -> Response:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "Existe déjà !"},
        )

    @app.exception_handler(CannotDeleteError)
    async def cannot_delete_exception_handler(
        request: Request,
        exc: CannotDeleteError,
    ) -> Response:
        message = f"'{exc.item_name}' ne peut pas être supprimé"
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": message},
        )
