from typing import Any

from app.domain.shops.entities import Shop
from app.domain.users.entities import User


def to_user_domain(user: dict[str, Any], shops: list[dict[str, Any]]) -> User:
    return User(
        id=str(user["_id"]),
        name=user["name"],
        username=user["username"],
        email=user["email"],
        hashed_password=user["password"],
        shops=[
            Shop(
                id=str(shop["_id"]),
                name=shop["name"],
                username=shop["username"],
                margins=shop["margins"],
            )
            for shop in shops
        ],
        role=user["role"],
    )
