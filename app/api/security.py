import jwt
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher
from pydantic import BaseModel

password_hash = PasswordHash((Argon2Hasher(), BcryptHasher()))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> tuple[bool, str | None]:
    return password_hash.verify_and_update(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def create_access_token(sub: str, secret_key: str) -> str:
    return jwt.encode({"sub": sub}, secret_key, algorithm="HS256")
