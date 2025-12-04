from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

from app.api.dependencies import (
    get_domain,
    get_optional_current_user,
    get_settings,
    get_templates,
)
from app.api.security.entities import JWTToken, TokenType
from app.api.security.password import verify_password
from app.core.config.settings import Settings
from app.domain.domain import Domain
from app.domain.users.entities import User, UserUpdate

LOGIN_ERROR_MESSAGE = "Email ou mot de passe incorrect"

router = APIRouter()


@router.get("/")
def home(
    request: Request,
    current_user: Annotated[User | None, Depends(get_optional_current_user)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
) -> Response:
    # A valid user is already logged in
    if current_user:
        return RedirectResponse(
            url=request.url_for("get_articles"),
            status_code=status.HTTP_302_FOUND,
        )

    error = request.session.pop("login_error", None)
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error": error},
    )


@router.post("/")
def login(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    settings: Annotated[Settings, Depends(get_settings)],
    domain: Annotated[Domain, Depends(get_domain)],
) -> Response:
    user = domain.get_user_by_email(email=form_data.username)
    if not user:
        request.session["login_error"] = LOGIN_ERROR_MESSAGE
        return RedirectResponse(
            url=request.url_for("home"),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    valid_password, updated_hash = verify_password(
        plain_password=form_data.password,
        hashed_password=user.hashed_password,
    )
    if updated_hash is not None:
        user_update = UserUpdate(hashed_password=updated_hash)
        domain.update_user(user_id=user.id, user_update=user_update)

    if not valid_password:
        request.session["login_error"] = LOGIN_ERROR_MESSAGE
        return RedirectResponse(
            url=request.url_for("home"),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    access_token = JWTToken.from_sub(
        sub=user.email,
        token_type=TokenType.ACCESS,
        settings=settings,
    )
    refresh_token = JWTToken.from_sub(
        sub=user.email,
        token_type=TokenType.REFRESH,
        settings=settings,
    )
    response = RedirectResponse(
        url=request.url_for("get_articles"),
        status_code=status.HTTP_302_FOUND,
    )
    access_cookie = access_token.to_cookie(settings)
    response.set_cookie(
        key=access_cookie.key,
        value=access_cookie.value,
        max_age=access_cookie.max_age,
        secure=access_cookie.secure,
        httponly=access_cookie.httponly,
        samesite=access_cookie.samesite,
    )
    refresh_cookie = refresh_token.to_cookie(settings)
    response.set_cookie(
        key=refresh_cookie.key,
        value=refresh_cookie.value,
        max_age=refresh_cookie.max_age,
        secure=refresh_cookie.secure,
        httponly=refresh_cookie.httponly,
        samesite=refresh_cookie.samesite,
    )
    return response


@router.get("/logout")
def logout(request: Request) -> Response:
    request.session.clear()
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return response
