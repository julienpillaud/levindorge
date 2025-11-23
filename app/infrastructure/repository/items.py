from bson import ObjectId
from cleanstack.exceptions import NotFoundError
from cleanstack.infrastructure.mongo.entities import MongoDocument
from pymongo.collection import Collection

from app.domain._shared.protocols.repository import ItemRepositoryProtocol
from app.domain.entities import EntityId
from app.domain.items.entities import Item, ItemType
from app.domain.volumes.entities import Volume
from app.infrastructure.repository.protocol import MongoRepositoryProtocol

FIELD_MAP = {
    ItemType.DISTRIBUTORS: "distributor",
    ItemType.COUNTRIES: "region",
    ItemType.REGIONS: "region",
}


class ItemRepository(MongoRepositoryProtocol, ItemRepositoryProtocol):
    def _get_collection(self, name: ItemType) -> Collection[MongoDocument]:
        return self.database.get_collection(name)

    def get_item(self, item_type: ItemType, item_id: EntityId) -> Item | None:
        collection = self._get_collection(name=item_type)
        item = collection.find_one({"_id": ObjectId(item_id)})
        return Item(**item) if item else None

    def item_exists(self, item_type: ItemType, item: Item) -> bool:
        collection = self._get_collection(name=item_type)
        result = collection.find_one({"name": item.name})
        return result is not None

    def create_item(self, item_type: ItemType, item: Item) -> Item:
        collection = self._get_collection(name=item_type)
        result = collection.insert_one(item.model_dump(exclude={"id"}))
        return self._get_item_by_id(collection=collection, item_id=result.inserted_id)

    def get_items(self, item_type: ItemType) -> list[Item]:
        collection = self._get_collection(name=item_type)
        return [Item.to_domain_entity(item) for item in collection.find().sort("name")]

    def delete_item(self, item_type: ItemType, item: Item) -> None:
        collection = self._get_collection(name=item_type)
        collection.delete_one({"_id": ObjectId(item.id)})

    def item_is_used(self, item_type: ItemType, item: Item) -> bool:
        field = FIELD_MAP.get(item_type)
        if not field:
            return False
        article = self.database["articles"].find_one({field: item.name})
        return article is not None

    def get_volumes_by_category(self, volume_category: str | None) -> list[Volume]:
        return [
            Volume.to_domain_entity(volume)
            for volume in self.database["volumes"]
            .find({"category": volume_category})
            .sort("value")
        ]

    @staticmethod
    def _get_item_by_id(
        collection: Collection[MongoDocument],
        item_id: str,
    ) -> Item:
        item_db = collection.find_one({"_id": ObjectId(item_id)})
        if not item_db:
            raise NotFoundError()

        return Item(**item_db)
