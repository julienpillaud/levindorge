from typing import Any

from bson import ObjectId
from cleanstack.exceptions import NotFoundError

from app.domain.entities import EntityId
from app.domain.protocols.repository import UserRepositoryProtocol
from app.domain.users.entities import User
from app.infrastructure.repository.protocol import MongoRepositoryProtocol


class UserRepository(MongoRepositoryProtocol, UserRepositoryProtocol):
    def get_user(self, user_id: EntityId) -> User | None:
        return self._get_user_by_filter({"_id": ObjectId(user_id)})

    def get_user_by_email(self, email: str) -> User | None:
        return self._get_user_by_filter({"email": email})

    def update_user(self, user: User) -> User:
        self.database["users"].replace_one(
            {"_id": ObjectId(user.id)},
            user.model_dump(exclude={"id", "shops"}),
        )
        user_db = self._get_user_by_filter({"_id": ObjectId(user.id)})
        if not user_db:
            raise NotFoundError()

        return user_db

    def _get_user_by_filter(self, match_filter: dict[str, Any]) -> User | None:
        user = self.database["users"].find_one(match_filter)
        if not user:
            return None

        user["shops"] = list(self.database["shops"].find())

        return User(**user)
