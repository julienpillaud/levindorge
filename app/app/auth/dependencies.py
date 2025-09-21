from typing import Annotated

import jwt
from cleanstack.exceptions import BadRequestError
from fastapi import Depends
from fastapi.params import Query
from fastapi.requests import Request

from app.app.dependencies import get_domain, get_settings
from app.core.config import Settings
from app.domain.domain import Domain
from app.domain.exceptions import UserUnauthorizedError
from app.domain.shops.entities import Shop
from app.domain.users.entities import User


def get_token_scheme_param(authorization: str | None) -> tuple[str, str]:
    if not authorization:
        return "", ""
    scheme, _, param = authorization.partition(" ")
    return scheme, param


def _get_user_from_token(
    request: Request,
    settings: Settings,
    domain: Domain,
) -> User | None:
    authorization = request.cookies.get("access_token")
    scheme, param = get_token_scheme_param(authorization=authorization)
    if not authorization or scheme.lower() != "bearer":
        return None

    try:
        payload = jwt.decode(param, settings.secret_key, algorithms=["HS256"])
    except jwt.PyJWTError:
        return None

    email = payload.get("sub")
    if not email:
        return None

    user = request.session.get("current_user")
    if user:
        return User(**user)

    user = domain.get_user_by_email(email=email)
    if not user:
        return None

    request.session["current_user"] = user.model_dump()
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


def get_current_shop(
    current_user: Annotated[User, Depends(get_current_user)],
    shop: Annotated[str, Query()],
) -> Shop:
    for user_shop in current_user.shops:
        if shop == user_shop.username:
            return user_shop
    raise BadRequestError("Invalid shop")
