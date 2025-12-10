from typing import Any

from rich import print

from app.core.core import Context
from app.domain.stores.entities import Store
from app.domain.users.entities import User


def create_users(
    src_context: Context,
    dst_context: Context,
    stores: list[Store],
) -> list[User]:
    # Get previous users
    src_users = list(src_context.database["users"].find())
    # Create users with the new entity model
    dst_users = create_user_entities(src_users=src_users, stores=stores)

    # Save users in the database
    result = dst_context.user_repository.create_many(dst_users)
    count = len(result)
    print(f"Created {count} users ({len(src_users)})")
    return dst_context.user_repository.get_all(limit=count).items


def create_user_entities(
    src_users: list[dict[str, Any]],
    stores: list[Store],
) -> list[User]:
    return []
