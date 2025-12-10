import logging
from functools import lru_cache
from typing import Annotated, cast

from fastapi import Depends, Form
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.api.security.token import decode_jwt
from app.api.utils import init_templates
from app.core.config.settings import Settings
from app.domain.domain import Domain
from app.domain.exceptions import UserUnauthorizedError
from app.domain.users.entities import User

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # ty:ignore[missing-argument]


def get_domain(request: Request) -> Domain:
    return cast(Domain, request.app.state.domain)


@lru_cache(maxsize=1)
def get_templates(
    settings: Annotated[Settings, Depends(get_settings)],
) -> Jinja2Templates:
    return init_templates(settings=settings)


def _get_user_from_token(request: Request, settings: Settings) -> User | None:
    access_token = request.state.new_access_token or request.cookies.get("access_token")
    if not access_token:
        return None

    token = decode_jwt(access_token, settings=settings)
    if not token:
        return None

    return User(id=token.sub, email=token.email)


def get_current_user(
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
) -> User:
    user = _get_user_from_token(request=request, settings=settings)
    if not user:
        raise UserUnauthorizedError("Invalid token")

    return user


def get_optional_current_user(
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
) -> User | None:
    return _get_user_from_token(request=request, settings=settings)


def get_optional_current_user_from_form(
    settings: Annotated[Settings, Depends(get_settings)],
    access_token: Annotated[str, Form()],
) -> User | None:
    if not access_token:
        return None

    token = decode_jwt(access_token, settings=settings)
    if not token:
        return None

    return User(id=token.sub, email=token.email)
