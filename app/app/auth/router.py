from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

from app.app.auth.dependencies import get_optional_current_user
from app.app.auth.security import create_access_token, verify_password
from app.app.dependencies import get_domain, get_settings, get_templates
from app.app.utils import url_for_with_query
from app.core.config import Settings
from app.domain.commons.entities import DisplayGroup
from app.domain.domain import Domain
from app.domain.users.entities import User

router = APIRouter()


@router.get("/")
def home(
    request: Request,
    current_user: Annotated[User | None, Depends(get_optional_current_user)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
) -> Response:
    # A valid user is already logged in
    if current_user:
        url = url_for_with_query(
            request,
            name="get_articles_view",
            list_category=DisplayGroup.BEER,
            query_params={"shop": current_user.shops[0].username},
        )
        return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)

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
    if not user or not verify_password(form_data.password, user.hashed_password):
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "Email ou mot de passe incorrect"},
        )

    access_token = create_access_token(sub=user.email, secret_key=settings.secret_key)

    url = url_for_with_query(
        request,
        name="get_articles_view",
        list_category=DisplayGroup.BEER,
        query_params={"shop": user.shops[0].username},
    )
    response = RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)
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
