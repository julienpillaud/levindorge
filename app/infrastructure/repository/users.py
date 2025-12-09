from app.domain.users.entities import User
from app.domain.users.repository import UserRepositoryProtocol
from app.infrastructure.repository.mongo_repository import (
    MongoDocument,
    MongoRepository,
)


class UserRepository(MongoRepository[User], UserRepositoryProtocol):
    domain_entity_type = User
    collection_name = "users"

    def get_by_email(self, email: str, /) -> User | None:
        return self.get_one({"email": email})

    @staticmethod
    def _to_database_entity(entity: User, /) -> MongoDocument:
        document = entity.model_dump(exclude={"id"})
        # document["stores"] = [store.slug for store in entity.stores]
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
