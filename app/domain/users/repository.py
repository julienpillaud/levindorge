from typing import Protocol

from app.domain._shared.protocols.base_repository import RepositoryProtocol
from app.domain.users.entities import User


class UserRepositoryProtocol(RepositoryProtocol[User], Protocol):
    def get_by_email(self, email: str, /) -> User | None: ...
