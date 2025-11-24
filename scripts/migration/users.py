from typing import Any

from rich import print

from app.core.core import Context
from app.domain.stores.entities import Store
from app.domain.users.entities import Role, User


def create_users(
    src_context: Context,
    dst_context: Context,
    stores: list[Store],
) -> list[User]:
    # Get previous users
    src_users = src_context.database["users"].find()
    # Create users with the new entity model
    dst_users = create_user_entities(src_users=list(src_users), stores=stores)

    # Save users in the database
    result = dst_context.user_repository.create_many(dst_users)
    count = len(result)
    print(f"Created {count} users")
    return dst_context.user_repository.get_all(limit=count).items


def create_user_entities(
    src_users: list[dict[str, Any]],
    stores: list[Store],
) -> list[User]:
    stores_map = {store.slug: store for store in stores}

    dst_users = [
        User(
            name=user["name"],
            email=user["email"],
            hashed_password=user["password"],
            stores=[stores_map[store_slug] for store_slug in user["shops"]],
            role=user["role"],
        )
        for user in src_users
    ]
    super_admin_user = User(
        name="Super Admin",
        email="superadmin@levindorge.com",
        hashed_password="$argon2id$v=19$m=65536,t=3,p=4$ndR3enkNQTou1m5vg12BYw$j76aDP0Z9/c60VtcybA+fUezK9T/0SJVyBpWa4DvEIA",
        stores=stores,
        role=Role.SUPERADMIN,
    )
    dst_users.append(super_admin_user)
    return dst_users
