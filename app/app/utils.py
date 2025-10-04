from typing import Any
from urllib.parse import urlencode

from fastapi import FastAPI
from fastapi.datastructures import URL
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from app.app.filters import (
    create_local_timezone_filter,
    get_flashed_messages,
    get_navbar_category_title,
    strip_zeros,
)
from app.core.config import Settings
from app.data import navbar_categories


def init_templates(settings: Settings) -> Jinja2Templates:
    templates = Jinja2Templates(directory=settings.app_path.templates)

    templates.env.globals["navbar_categories"] = navbar_categories
    templates.env.globals["get_flashed_messages"] = get_flashed_messages

    templates.env.filters["strip_zeros"] = strip_zeros
    templates.env.filters["get_navbar_category_title"] = get_navbar_category_title
    templates.env.filters["local_timezone"] = create_local_timezone_filter(
        zone_info=settings.zone_info
    )
    return templates


def mount_static(app: FastAPI, settings: Settings) -> None:
    app.mount(
        path="/static",
        app=StaticFiles(directory=settings.app_path.static),
        name="static",
    )


def add_session_middleware(app: FastAPI, settings: Settings) -> None:
    app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)


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
