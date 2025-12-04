from functools import lru_cache
from typing import Annotated, cast

from cleanstack.exceptions import BadRequestError
from fastapi import Depends, Query
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.api.security.entities import TokenType
from app.api.security.token import decode_token_string
from app.api.utils import init_templates
from app.core.config.settings import Settings
from app.domain.domain import Domain
from app.domain.exceptions import UserUnauthorizedError
from app.domain.stores.entities import Store
from app.domain.users.entities import User


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


def get_domain(request: Request) -> Domain:
    return cast(Domain, request.app.state.domain)


@lru_cache(maxsize=1)
def get_templates(
    settings: Annotated[Settings, Depends(get_settings)],
) -> Jinja2Templates:
    return init_templates(settings=settings)


def _get_user_from_token(
    request: Request,
    settings: Settings,
    domain: Domain,
) -> User | None:
    access_token = request.state.new_access_token or request.cookies.get("access_token")
    token = decode_token_string(access_token, settings=settings)
    if not token:
        return None

    if token.type != TokenType.ACCESS:
        return None

    user = domain.get_user_by_email(email=token.sub)
    if not user:
        return None

    return user


def get_current_user(
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
    domain: Annotated[Domain, Depends(get_domain)],
) -> User:
    user = _get_user_from_token(
        request=request,
        settings=settings,
        domain=domain,
    )
    if not user:
        raise UserUnauthorizedError("Invalid token")

    return user


def get_optional_current_user(
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
    domain: Annotated[Domain, Depends(get_domain)],
) -> User | None:
    return _get_user_from_token(
        request=request,
        settings=settings,
        domain=domain,
    )


def get_current_store(
    current_user: Annotated[User, Depends(get_current_user)],
    store: Annotated[str, Query()],
) -> Store:
    for user_store in current_user.stores:
        if store == user_store.slug:
            return user_store
    raise BadRequestError("Invalid shop")
