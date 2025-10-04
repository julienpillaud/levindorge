from cleanstack.exceptions import DomainError
from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, Response
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.app.dependencies import get_templates
from app.core.config import Settings
from app.domain.exceptions import (
    CannotDeleteError,
    DepositInUseError,
    UserUnauthorizedError,
    VolumeInUseError,
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
        redirect_map = {
            VolumeInUseError: "get_volumes_view",
            DepositInUseError: "get_deposits_view",
        }
        exception_class = type(exc)
        route_name = redirect_map.get(exception_class, "get_items_view")
        url_params = {"item_type": exc.item_type} if exc.item_type else {}

        message = f"'{exc.item_name}' ne peut pas être supprimé"
        request.session["_messages"] = [("danger", message)]

        return RedirectResponse(
            url=request.url_for(route_name, **url_params),
            status_code=status.HTTP_302_FOUND,
        )
