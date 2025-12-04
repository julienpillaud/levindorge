import jwt
from pydantic import ValidationError

from app.api.security.entities import ALGORITHM, JWTToken, TokenPayload, TokenType
from app.core.config.settings import Settings


def decode_token_string(
    value: str | None,
    /,
    settings: Settings,
) -> TokenPayload | None:
    if not value:
        return None

    scheme, _, param = value.partition(" ")
    if scheme.lower() != "bearer":
        return None

    try:
        payload = jwt.decode(param, settings.secret_key, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return None

    try:
        return TokenPayload(**payload)
    except ValidationError:
        return None


def create_access_from_refresh(
    value: str | None,
    /,
    settings: Settings,
) -> JWTToken | None:
    token = decode_token_string(value, settings=settings)
    if not token:
        return None

    return JWTToken.from_sub(
        sub=token.sub,
        token_type=TokenType.ACCESS,
        settings=settings,
    )
