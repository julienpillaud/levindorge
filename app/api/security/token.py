import jwt
from pydantic import BaseModel, ValidationError

from app.core.config.settings import Settings


class TokenPayload(BaseModel):
    sub: str
    exp: int
    iat: int
    email: str


def decode_jwt(value: str, /, settings: Settings) -> TokenPayload | None:
    if not value:
        return None

    try:
        payload = jwt.decode(
            value,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
            audience=settings.jwt_audience,
        )
    except jwt.PyJWTError:
        return None

    try:
        return TokenPayload(**payload)
    except ValidationError:
        return None
