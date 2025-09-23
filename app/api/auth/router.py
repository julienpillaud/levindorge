from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import get_domain, get_settings
from app.api.security import Token, create_access_token, verify_password
from app.core.config import Settings
from app.domain.domain import Domain

router = APIRouter()


@router.post("/token")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    settings: Annotated[Settings, Depends(get_settings)],
    domain: Annotated[Domain, Depends(get_domain)],
) -> Token:
    user = domain.get_user_by_email(email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token(sub=user.email, secret_key=settings.secret_key)
    return Token(access_token=access_token, token_type="bearer")
