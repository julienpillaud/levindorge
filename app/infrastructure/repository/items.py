from typing import Any

from cleanstack.infrastructure.mongo.entities import MongoDocument
from pymongo import ASCENDING, DESCENDING
from pymongo.collection import Collection

from app.domain.items.entities import Deposit, Item, Volume
from app.domain.protocols.repository import ItemRepositoryProtocol


class ItemRepository(ItemRepositoryProtocol):
    def _get_collection(self, name: str) -> Collection[MongoDocument]:
        return self.database.get_collection(name)

    def get_items_dict(self, volume_category: str | None) -> dict[str, Any]:
        return {
            "country_list": self.get_items("countries"),
            "region_list": self.get_items("regions"),
            "brewery_list": self.get_items("breweries"),
            "distillery_list": self.get_items("distilleries"),
            "distributor_list": self.get_items("distributors"),
            "volumes": self.get_volumes_by_category(volume_category),
            "deposits": self.get_deposits(),
        }

    def get_items(self, name: str) -> list[Item]:
        collection = self._get_collection(name=name)
        return [Item(**item) for item in collection.find().sort("name")]

    def get_volumes_by_category(self, volume_category: str | None) -> list[Volume]:
        return [
            Volume(**volume)
            for volume in self.database["volumes"]
            .find({"category": volume_category})
            .sort("value")
        ]

    def get_volumes(self) -> list[Volume]:
        return [
            Volume(**volume)
            for volume in self.database["volumes"]
            .find()
            .sort(
                [
                    ("category", ASCENDING),
                    ("value", ASCENDING),
                ]
            )
        ]

    def get_deposits(self) -> list[Deposit]:
        return [
            Deposit(**item)
            for item in self.database["deposits"]
            .find()
            .sort(
                [
                    ("category", ASCENDING),
                    ("deposit_type", DESCENDING),
                    ("value", ASCENDING),
                ]
            )
        ]
