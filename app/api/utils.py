import logging
from collections.abc import Awaitable, Callable
from typing import Any, Literal
from urllib.parse import urlencode

from fastapi import FastAPI
from fastapi.datastructures import URL
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import Response

from app.api.filters import (
    article_shops_to_json,
    create_local_timezone_filter,
    strip_zeros,
)
from app.api.navbar import navbar_categories, navbar_items
from app.api.security.token import decode_jwt
from app.core.config.settings import Settings

logger = logging.getLogger(__name__)


def init_templates(settings: Settings) -> Jinja2Templates:
    templates = Jinja2Templates(directory=settings.app_path.templates)

    templates.env.globals["navbar_categories"] = navbar_categories
    templates.env.globals["navbar_items"] = navbar_items
    templates.env.globals["app_version"] = settings.app_version

    templates.env.filters["strip_zeros"] = strip_zeros
    templates.env.filters["local_timezone"] = create_local_timezone_filter(
        zone_info=settings.zone_info
    )
    templates.env.filters["article_shops_to_json"] = article_shops_to_json
    return templates


def mount_static(app: FastAPI, settings: Settings) -> None:
    app.mount(
        path="/static",
        app=StaticFiles(directory=settings.app_path.static),
        name="static",
    )


def add_session_middleware(app: FastAPI, settings: Settings) -> None:
    app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)


def add_security_middleware(app: FastAPI, settings: Settings) -> None:
    @app.middleware("http")
    async def security_middleware(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        request.state.new_access_token = None

        access_token = request.cookies.get("access_token")
        refresh_token = request.cookies.get("refresh_token")

        # Access token is valid -> continue
        if access_token and decode_jwt(access_token, settings=settings):
            return await call_next(request)

        # No refresh token -> continue
        if not refresh_token:
            return await call_next(request)

        # Access token is invalid -> refresh it
        logger.debug("Refreshing access token...")
        user = app.state.domain.refresh_token(token=refresh_token)
        if not user:
            logger.warning("Failed to refresh access token")
            return await call_next(request)

        request.state.new_access_token = user.credentials.access_token
        response = await call_next(request)
        set_cookie(
            response,
            key="access_token",
            value=user.credentials.access_token,
            max_age=settings.access_token_expire,
        )
        set_cookie(
            response,
            key="refresh_token",
            value=user.credentials.refresh_token,
            max_age=settings.refresh_token_expire,
        )
        return response


def set_cookie(
    response: Response,
    /,
    key: str,
    value: str,
    max_age: int,
    secure: bool = True,
    httponly: bool = True,
    samesite: Literal["lax", "strict", "none"] = "lax",
) -> None:
    response.set_cookie(
        key=key,
        value=value,
        max_age=max_age,
        secure=secure,
        httponly=httponly,
        samesite=samesite,
    )


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
