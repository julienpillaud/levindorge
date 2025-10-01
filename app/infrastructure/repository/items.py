from bson import ObjectId
from cleanstack.infrastructure.mongo.entities import MongoDocument
from pymongo.collection import Collection

from app.domain.items.entities import Item, ItemType, Volume
from app.domain.protocols.repository import ItemRepositoryProtocol

FIELD_MAP = {
    ItemType.BREWERIES: "name.name1",
    ItemType.DISTILLERIES: "name.name1",
    ItemType.DISTRIBUTORS: "distributor",
    ItemType.COUNTRIES: "region",
    ItemType.REGIONS: "region",
}


class ItemRepository(ItemRepositoryProtocol):
    def _get_collection(self, name: ItemType) -> Collection[MongoDocument]:
        return self.database.get_collection(name)

    def get_item(self, item_type: ItemType, item_id: str) -> Item | None:
        collection = self._get_collection(name=item_type)
        item = collection.find_one({"_id": ObjectId(item_id)})
        return Item(**item) if item else None

    def get_items(self, item_type: ItemType) -> list[Item]:
        collection = self._get_collection(name=item_type)
        return [Item(**item) for item in collection.find().sort("name")]

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
            Volume(**volume)
            for volume in self.database["volumes"]
            .find({"category": volume_category})
            .sort("value")
        ]
