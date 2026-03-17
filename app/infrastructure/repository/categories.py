from cleanstack.infrastructure.mongo.base import MongoRepository, MongoRepositoryError

from app.domain.categories.entities import Category
from app.domain.categories.repository import CategoryRepositoryProtocol


class CategoryRepository(MongoRepository[Category], CategoryRepositoryProtocol):
    domain_entity_type = Category
    collection_name = "categories"
    searchable_fields = ()

    def create_many(self, categories: list[Category]) -> list[Category]:
        entities = [self._to_database_entity(entity) for entity in categories]

        result = self.collection.insert_many(entities)
        if not result.acknowledged:
            raise MongoRepositoryError("Failed to insert entities")

        return categories

    def get_by_name(self, name: str) -> Category | None:
        category = self.collection.find_one({"name": name})
        return self._to_domain_entity(category) if category else None
