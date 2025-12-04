import datetime
from enum import StrEnum
from typing import Literal

import jwt
from pydantic import BaseModel

from app.core.config.settings import AppEnvironment, Settings

ALGORITHM = "HS256"


class TokenType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"


class Cookie(BaseModel):
    key: str
    value: str
    max_age: int
    secure: bool
    httponly: bool = True
    samesite: Literal["lax", "strict", "none"]


class TokenPayload(BaseModel):
    sub: str
    exp: datetime.datetime
    type: TokenType


class JWTToken(BaseModel):
    token: str
    type: TokenType
    max_age: int  # in seconds

    @classmethod
    def from_sub(
        cls,
        sub: str,
        token_type: TokenType,
        settings: Settings,
    ) -> JWTToken:
        expires_delta = get_expires_delta(token_type=token_type, settings=settings)
        token = encode_jwt(
            token_type=token_type,
            sub=sub,
            expires_delta=expires_delta,
            settings=settings,
        )
        return cls(
            token=token,
            type=token_type,
            max_age=int(expires_delta.total_seconds()),
        )

    def to_cookie(self, settings: Settings, /) -> Cookie:
        return Cookie(
            key=f"{self.type}_token",
            value=f"Bearer {self.token}",
            max_age=self.max_age,
            secure=settings.environment == AppEnvironment.PRODUCTION,
            samesite="strict"
            if settings.environment == AppEnvironment.PRODUCTION
            else "lax",
        )


def get_expires_delta(token_type: TokenType, settings: Settings) -> datetime.timedelta:
    match token_type:
        case TokenType.ACCESS:
            return datetime.timedelta(minutes=settings.access_token_expire)
        case TokenType.REFRESH:
            return datetime.timedelta(minutes=settings.refresh_token_expire)


def encode_jwt(
    token_type: TokenType,
    sub: str,
    expires_delta: datetime.timedelta,
    settings: Settings,
) -> str:
    current_date = datetime.datetime.now(datetime.UTC)
    expire = current_date + expires_delta
    return jwt.encode(
        payload={"sub": sub, "exp": expire, "type": token_type},
        key=settings.secret_key,
        algorithm=ALGORITHM,
    )
