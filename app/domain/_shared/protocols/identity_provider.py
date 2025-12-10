from typing import Protocol

from app.domain.users.entities import User, UserWithCredentials


class IdentityProviderProtocol(Protocol):
    def sign_in_with_password(
        self,
        email: str,
        password: str,
    ) -> UserWithCredentials | None: ...

    def get_user(self, token: str) -> User | None: ...

    def refresh_token(self, token: str) -> UserWithCredentials | None: ...
