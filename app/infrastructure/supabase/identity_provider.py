from supabase import Client
from supabase.lib.client_options import SyncClientOptions
from supabase_auth.errors import AuthApiError

from app.core.config.settings import Settings
from app.domain.entities import EntityId
from app.domain.protocols.identity_provider import IdentityProviderProtocol
from app.domain.users.entities import User, UserCredentials, UserWithCredentials


class SupabaseIdentityProvider(IdentityProviderProtocol):
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    @property
    def client(self) -> Client:
        return Client(
            supabase_url=self.settings.supabase_url,
            supabase_key=self.settings.supabase_key,
            options=SyncClientOptions(
                auto_refresh_token=False,
                persist_session=False,
            ),
        )

    def update_user_password(self, user_id: EntityId, password: str) -> User | None:
        try:
            response = self.client.auth.admin.update_user_by_id(
                user_id,
                {"password": password},
            )
        except AuthApiError:
            return None

        if not response.user:
            return None

        return User(
            id=response.user.id,
            email=response.user.email or "",  # email should exist
        )

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
            email=response.user.email or "",  # email should exist
            credentials=UserCredentials(
                access_token=response.session.access_token,
                refresh_token=response.session.refresh_token,
                expires_in=response.session.expires_in,
            ),
        )

    def refresh_token(self, token: str) -> UserWithCredentials | None:
        try:
            response = self.client.auth.refresh_session(refresh_token=token)
        except AuthApiError:
            return None

        if not response.session or not response.user:
            return None

        return UserWithCredentials(
            id=response.user.id,
            email=response.user.email or "",  # email should exist
            credentials=UserCredentials(
                access_token=response.session.access_token,
                refresh_token=response.session.refresh_token,
                expires_in=response.session.expires_in,
            ),
        )
