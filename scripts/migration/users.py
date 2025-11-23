from app.core.core import Context
from app.domain.users.entities import Role, User


def update_users(src_context: Context, dst_context: Context) -> None:
    # New stores must be created before users
    stores = dst_context.store_repository.get_all()
    stores_map = {store.slug: store for store in stores.items}

    # Get previous users
    src_users = src_context.database["users"].find()
    # Create users with the new entity model
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
    dst_users.append(
        User(
            name="Super Admin",
            email="superadmin@levindorge.com",
            hashed_password="$argon2id$v=19$m=65536,t=3,p=4$ndR3enkNQTou1m5vg12BYw$j76aDP0Z9/c60VtcybA+fUezK9T/0SJVyBpWa4DvEIA",
            stores=stores.items,
            role=Role.SUPERADMIN,
        )
    )
    # Save users in the database
    dst_context.user_repository.create_many(dst_users)
