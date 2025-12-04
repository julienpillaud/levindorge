import logging
from collections.abc import Awaitable, Callable
from typing import Any
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
from app.api.security.token import create_access_from_refresh, decode_token_string
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

        # Access token is valid -> continue
        access_token_str = request.cookies.get("access_token")
        access_token = decode_token_string(access_token_str, settings=settings)
        logger.debug("Access token", extra={"access_token": access_token})
        if access_token:
            return await call_next(request)

        # Access token is invalid -> refresh it
        refresh_token_str = request.cookies.get("refresh_token")
        refresh_token = decode_token_string(refresh_token_str, settings=settings)
        logger.debug("Refresh token", extra={"refresh_token": refresh_token})
        if refresh_token:
            new_access_token = create_access_from_refresh(
                refresh_token_str,
                settings=settings,
            )
            logger.debug(
                "New access token", extra={"new_access_token": new_access_token}
            )
            if not new_access_token:
                logger.debug("Failed to create new access token")
                return await call_next(request)

            cookie = new_access_token.to_cookie(settings)
            request.state.new_access_token = cookie.value
            response = await call_next(request)
            response.set_cookie(
                key=cookie.key,
                value=cookie.value,
                max_age=cookie.max_age,
                secure=cookie.secure,
                httponly=cookie.httponly,
                samesite=cookie.samesite,
            )
            return response

        # Refresh token is invalid -> redirect to home
        return await call_next(request)


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
