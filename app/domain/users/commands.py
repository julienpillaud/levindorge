from app.domain.context import ContextProtocol
from app.domain.users.entities import User, UserWithCredentials


def update_user_password_command(
    context: ContextProtocol,
    /,
    user_id: str,
    password: str,
) -> User | None:
    return context.identity_provider.update_user_password(
        user_id=user_id,
        password=password,
    )


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


def refresh_token_command(
    context: ContextProtocol,
    /,
    token: str,
) -> UserWithCredentials | None:
    return context.identity_provider.refresh_token(token=token)
