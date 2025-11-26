from typing import TypedDict

from app.domain.users.entities import Role, User
from app.domain.users.repository import UserRepositoryProtocol
from app.infrastructure.repository.mongo_repository import (
    MongoDocument,
    MongoRepository,
)


class UserDocument(TypedDict):
    _id: str
    name: str
    email: str
    hashed_password: str
    stores: list[str]
    role: Role


class UserRepository(MongoRepository[User], UserRepositoryProtocol):
    domain_entity_type = User
    collection_name = "users"

    def get_by_email(self, email: str, /) -> User | None:
        user = self.collection.find_one({"email": email})
        if not user:
            return None

        user["stores"] = list(self.database["stores"].find().sort("name"))
        return User(**user)

    @staticmethod
    def _to_database_entity(entity: User, /) -> MongoDocument:
        document = entity.model_dump(exclude={"id"})
        document["stores"] = [store.slug for store in entity.stores]
        return document

    @staticmethod
    def _aggregation_pipeline() -> list[MongoDocument]:
        return [
            {
                "$lookup": {
                    "from": "stores",
                    "let": {"slugs": "$stores"},
                    "pipeline": [{"$match": {"$expr": {"$in": ["$slug", "$$slugs"]}}}],
                    "as": "stores",
                }
            }
        ]
