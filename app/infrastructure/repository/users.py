from app.domain.protocols.repository import UserRepositoryProtocol
from app.domain.shops.entities import Shop
from app.domain.users.entities import User


class UserRepository(UserRepositoryProtocol):
    def get_user_by_email(self, email: str) -> User | None:
        user = self.database["users"].find_one({"email": email})
        if not user:
            return None

        shops = list(self.database["shops"].find({"username": {"$in": user["shops"]}}))

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
                    tactill_api_key=shop["tactill_api_key"],
                    margins=shop["margins"],
                )
                for shop in shops
            ],
            role=user["role"],
        )
