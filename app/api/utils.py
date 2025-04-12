from typing import Any
from urllib.parse import urlencode

from fastapi import FastAPI, status
from fastapi.datastructures import URL
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.api.dependencies import get_settings
from app.domain.exceptions import DomainError, NotAuthorizedError


def mount_static(app: FastAPI) -> None:
    app.mount(
        "/static",
        StaticFiles(directory="app/application/static"),
        name="static",
    )


def add_exceptions_handler(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def api_exception_handler(request: Request, error: DomainError) -> Response:
        if isinstance(error, NotAuthorizedError):
            return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


def add_session_middleware(app: FastAPI) -> None:
    settings = get_settings()
    app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)


def url_for_with_query(
    request: Request,
    name: str,
    *,
    query_params: dict[str, str] | None = None,
    **path_params: Any,
) -> URL:
    base_url = request.url_for(name, **path_params)

    if query_params:
        return URL(f"{base_url}?{urlencode(query_params)}")

    return base_url
