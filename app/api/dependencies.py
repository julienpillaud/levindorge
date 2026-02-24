from functools import lru_cache
from typing import Annotated

from fastapi import Depends, Form
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.api.logger import logger
from app.api.security.token import decode_jwt
from app.api.utils import init_templates
from app.core.config.settings import Settings
from app.core.context import Context
from app.core.uow import UnitOfWork
from app.domain.domain import Domain
from app.domain.exceptions import UserUnauthorizedError
from app.domain.users.entities import User
from app.infrastructure.repository.uow import MongoUnitOfWork


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


def get_mongo_uow(
    settings: Annotated[Settings, Depends(get_settings)],
) -> MongoUnitOfWork:
    return MongoUnitOfWork(settings=settings)


def get_uow(
    mongo_uow: Annotated[MongoUnitOfWork, Depends(get_mongo_uow)],
) -> UnitOfWork:
    return UnitOfWork(mongo=mongo_uow)


def get_context(
    settings: Annotated[Settings, Depends(get_settings)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> Context:
    return Context(settings=settings, uow=uow)


def get_domain(
    uow: Annotated[UnitOfWork, Depends(get_uow)],
    context: Annotated[Context, Depends(get_context)],
) -> Domain:
    return Domain(uow=uow, context=context)


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
    request.state.credentials = None
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    # Access token is valid -> continue
    if access_token:
        token = decode_jwt(access_token, settings=settings)
        if token:
            return User(id=token.sub, email=token.email)

    # No refresh token -> continue
    if not refresh_token:
        return None

    # Access token is invalid -> refresh it
    logger.debug("Refreshing access token...")
    user = domain.refresh_token(token=refresh_token)
    if not user:
        logger.warning("Failed to refresh access token")
        return None

    request.state.credentials = user.credentials
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
