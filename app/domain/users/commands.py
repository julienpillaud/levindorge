from app.domain.context import ContextProtocol
from app.domain.users.entities import User


def get_user_by_email_command(context: ContextProtocol, email: str) -> User | None:
    return context.repository.get_user_by_email(email=email)
