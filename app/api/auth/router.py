from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

from app.api.auth.dependencies import get_optional_current_user
from app.api.dependencies import get_domain, get_settings, get_templates
from app.api.security import create_access_token, verify_password
from app.core.config import Settings
from app.domain.domain import Domain
from app.domain.users.entities import User, UserUpdate

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

    return templates.TemplateResponse(request=request, name="login.html")


@router.post("/")
def login(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    settings: Annotated[Settings, Depends(get_settings)],
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
) -> Response:
    user = domain.get_user_by_email(email=form_data.username)
    if not user:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "Email ou mot de passe incorrect"},
        )

    valid_password, updated_hash = verify_password(
        plain_password=form_data.password,
        hashed_password=user.hashed_password,
    )
    if updated_hash is not None:
        user_update = UserUpdate(hashed_password=updated_hash)
        domain.update_user(user_id=user.id, user_update=user_update)

    if not valid_password:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "Email ou mot de passe incorrect"},
        )

    access_token = create_access_token(sub=user.email, secret_key=settings.secret_key)

    response = RedirectResponse(
        url=request.url_for("get_articles"),
        status_code=status.HTTP_302_FOUND,
    )
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
    )
    return response


@router.get("/logout")
def logout(request: Request) -> Response:
    request.session.clear()
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="access_token")
    return response
