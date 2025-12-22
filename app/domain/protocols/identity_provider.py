from typing import Protocol

from app.domain.users.entities import User, UserWithCredentials


class IdentityProviderProtocol(Protocol):
    def update_user_password(
        self,
        user_id: str,
        password: str,
    ) -> User | None: ...

    def sign_in_with_password(
        self,
        email: str,
        password: str,
    ) -> UserWithCredentials | None: ...

    def refresh_token(self, token: str) -> UserWithCredentials | None: ...
