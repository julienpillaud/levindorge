from cleanstack.exceptions import NotFoundError

from app.domain.context import ContextProtocol
from app.domain.entities import EntityId
from app.domain.users.entities import User, UserUpdate


def get_user_by_email_command(context: ContextProtocol, email: str) -> User | None:
    return context.user_repository.get_by_email(email)


def update_user_command(
    context: ContextProtocol,
    user_id: EntityId,
    user_update: UserUpdate,
) -> User:
    user = context.user_repository.get_by_id(user_id)
    if not user:
        raise NotFoundError()

    user.hashed_password = user_update.hashed_password

    return context.user_repository.update(user)
