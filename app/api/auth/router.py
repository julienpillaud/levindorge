from typing import Annotated

from fastapi import APIRouter, Depends, Form, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, Response

from app.api.auth.dependencies import get_optional_current_user
from app.api.auth.security import create_access_token, verify_password
from app.api.dependencies import get_domain, get_settings
from app.core.config import Settings
from app.core.templates import templates
from app.domain.domain import Domain
from app.domain.users.entities import User

router = APIRouter()


@router.get("/")
async def home(
    request: Request,
    current_user: Annotated[User | None, Depends(get_optional_current_user)],
) -> Response:
    # A valid user is already logged in
    if current_user:
        return RedirectResponse(url="/articles", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse(request=request, name="login.html")


@router.post("/")
async def login(
    request: Request,
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    settings: Annotated[Settings, Depends(get_settings)],
    domain: Annotated[Domain, Depends(get_domain)],
) -> Response:
    user = domain.get_user_by_email(email=username)
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "Email ou mot de passe incorrect"},
        )

    access_token = create_access_token(sub=user.email, secret_key=settings.SECRET_KEY)

    response = RedirectResponse(url="/articles", status_code=302)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
    )
    return response


@router.get("/logout")
async def logout() -> Response:
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="access_token")
    return response
