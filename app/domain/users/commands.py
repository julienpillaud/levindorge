from cleanstack.exceptions import NotFoundError

from app.domain.context import ContextProtocol
from app.domain.entities import EntityId
from app.domain.users.entities import User, UserUpdate


def get_user_by_email_command(context: ContextProtocol, email: str) -> User | None:
    return context.repository.get_user_by_email(email=email)


def update_user_command(
    context: ContextProtocol,
    user_id: EntityId,
    user_update: UserUpdate,
) -> User:
    user = context.repository.get_user(user_id=user_id)
    if not user:
        raise NotFoundError()

    user.hashed_password = user_update.hashed_password

    return context.repository.update_user(user=user)
