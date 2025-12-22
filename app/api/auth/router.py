from typing import Annotated

from fastapi import APIRouter, Depends, Form, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

from app.api.dependencies import (
    get_domain,
    get_optional_current_user,
    get_optional_current_user_from_form,
    get_settings,
    get_templates,
)
from app.api.utils import set_cookie
from app.core.config.settings import Settings
from app.domain.domain import Domain
from app.domain.users.entities import User

LOGIN_ERROR_MESSAGE = "Email ou mot de passe incorrect"

router = APIRouter(tags=["Auth"])


@router.get("/auth/register")
def register(
    request: Request,
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    access_token: str | None = None,
) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={"access_token": access_token},
    )


@router.post("/auth/register")
def set_password(
    request: Request,
    current_user: Annotated[User | None, Depends(get_optional_current_user_from_form)],
    domain: Annotated[Domain, Depends(get_domain)],
    password: Annotated[str, Form()],
) -> Response:
    if not current_user:
        request.session["error_message"] = "Erreur enregistrement mot de passe"
        return RedirectResponse(
            url=request.url_for("home"),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    domain.update_user_password(user_id=current_user.id, password=password)
    return RedirectResponse(
        url=request.url_for("home"),
        status_code=status.HTTP_303_SEE_OTHER,
    )


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

    error = request.session.pop("error_message", None)
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error": error},
    )


@router.post("/")
def login(
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
    domain: Annotated[Domain, Depends(get_domain)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Response:
    user = domain.sign_in_with_password(
        email=form_data.username,
        password=form_data.password,
    )
    if not user:
        request.session["error_message"] = LOGIN_ERROR_MESSAGE
        return RedirectResponse(
            url=request.url_for("home"),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    response = RedirectResponse(
        url=request.url_for("get_articles"),
        status_code=status.HTTP_302_FOUND,
    )
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


@router.get("/logout")
def logout(request: Request) -> Response:
    request.session.clear()
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return response
