from supabase import Client
from supabase_auth.errors import AuthApiError

from app.domain._shared.protocols.identity_provider import IdentityProviderProtocol
from app.domain.users.entities import User, UserCredentials, UserWithCredentials


class SupabaseIdentityProvider(IdentityProviderProtocol):
    def __init__(self, client: Client) -> None:
        self.client = client

    def sign_in_with_password(
        self,
        email: str,
        password: str,
    ) -> UserWithCredentials | None:
        try:
            response = self.client.auth.sign_in_with_password(
                credentials={"email": email, "password": password}
            )
        except AuthApiError:
            return None

        if not response.session or not response.user:
            return None

        return UserWithCredentials(
            id=response.user.id,
            email=response.user.email,
            credentials=UserCredentials(
                access_token=response.session.access_token,
                refresh_token=response.session.refresh_token,
                expires_in=response.session.expires_in,
            ),
        )

    def get_user(self, token: str) -> User | None:
        try:
            response = self.client.auth.get_user(jwt=token)
        except AuthApiError:
            return None

        if not response:
            return None

        return User(id=response.user.id, email=response.user.email or "")

    def refresh_token(self, token: str) -> UserWithCredentials | None:
        try:
            response = self.client.auth.refresh_session(refresh_token=token)
        except AuthApiError:
            return None

        if not response.session or not response.user:
            return None

        return UserWithCredentials(
            id=response.user.id,
            email=response.user.email or "",
            credentials=UserCredentials(
                access_token=response.session.access_token,
                refresh_token=response.session.refresh_token,
                expires_in=response.session.expires_in,
            ),
        )
