from cleanstack.exceptions import DomainError
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import Response
from starlette import status
from starlette.exceptions import HTTPException as StarletteHTTPException

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

    @app.exception_handler(CannotDeleteError)
    async def cannot_delete_exception_handler(
        request: Request,
        exc: CannotDeleteError,
    ) -> Response:
        message = f"'{exc.item_name}' ne peut pas être supprimé"
        return templates.TemplateResponse(
            request=request,
            name="errors/_error_toast.html",
            context={"message": message, "category": "danger"},
            status_code=status.HTTP_409_CONFLICT,
        )
