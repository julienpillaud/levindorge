from app.domain.context import ContextProtocol
from app.domain.users.entities import User, UserWithCredentials


def sign_in_with_password_command(
    context: ContextProtocol,
    /,
    email: str,
    password: str,
) -> UserWithCredentials | None:
    return context.identity_provider.sign_in_with_password(
        email=email,
        password=password,
    )


def get_user_command(context: ContextProtocol, token: str) -> User | None:
    return context.identity_provider.get_user(token=token)


def refresh_token_command(
    context: ContextProtocol,
    /,
    token: str,
) -> UserWithCredentials | None:
    return context.identity_provider.refresh_token(token=token)
