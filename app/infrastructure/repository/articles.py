from app.domain.articles.entities import Article
from app.domain.articles.repository import ArticleRepositoryProtocol
from app.domain.deposits.entities import Deposit
from app.domain.entities import (
    EntityId,
    PaginatedResponse,
    SortEntity,
    SortOrder,
)
from app.domain.filters import FilterEntity, FilterOperator
from app.domain.origins.entities import Origin
from app.domain.volumes.entities import Volume
from app.infrastructure.repository.base import MongoRepository


class ArticleRepository(MongoRepository[Article], ArticleRepositoryProtocol):
    domain_entity_type = Article
    collection_name = "articles"
    searchable_fields = (
        "reference",
        "category",
        "producer",
        "product",
        "distributor",
        "origin",
        "color",
        "taste",
    )

    def get_by_ids(self, article_ids: list[EntityId], /) -> PaginatedResponse[Article]:
        return self.get_all(
            filters=[
                FilterEntity(
                    field="id",
                    value=article_ids,
                    operator=FilterOperator.IN,
                )
            ],
            sort=[
                SortEntity(field="type", order=SortOrder.ASC),
                SortEntity(field="name.name1", order=SortOrder.ASC),
                SortEntity(field="name.name2", order=SortOrder.ASC),
            ],
        )

    def exists_by_producer(self, producer: str) -> bool:
        return self.collection.find_one({"producer": producer}) is not None

    def exists_by_distributor(self, distributor: str) -> bool:
        return self.collection.find_one({"distributor": distributor}) is not None

    def exists_by_deposit(self, deposit: Deposit) -> bool:
        return (
            self.collection.find_one({f"deposit.{deposit.type}": float(deposit.value)})
            is not None
        )

    def exists_by_volume(self, volume: Volume) -> bool:
        return (
            self.collection.find_one(
                {"volume.value": volume.value, "volume.unit": volume.unit}
            )
            is not None
        )

    def exists_by_origin(self, origin: Origin) -> bool:
        return self.collection.find_one({"origin": origin.name}) is not None
