from typing import Protocol

from app.domain.users.entities import User


class RepositoryProtocol(Protocol):
    def get_user_by_email(self, email: str) -> User | None: ...
