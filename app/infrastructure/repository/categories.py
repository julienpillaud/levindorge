from app.domain.categories.entities import Category
from app.domain.categories.repository import CategoryRepositoryProtocol
from app.infrastructure.repository.mongo_repository import MongoRepository


class CategoryRepository(MongoRepository[Category], CategoryRepositoryProtocol):
    domain_entity_type = Category
    collection_name = "categories"
    searchable_fields = ()

    def get_by_name(self, name: str) -> Category | None:
        category = self.collection.find_one({"name": name})
        return self._to_domain_entity(category) if category else None
