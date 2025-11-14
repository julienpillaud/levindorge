from app.domain.categories.entities import Category
from app.domain.categories.repository import CategoryRepositoryProtocol
from app.infrastructure.repository.mongo_repository import MongoRepository


class CategoryRepository(MongoRepository[Category], CategoryRepositoryProtocol):
    domain_model = Category
    collection_name = "categories"
    searchable_fields = ()
