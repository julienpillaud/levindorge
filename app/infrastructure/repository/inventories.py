from typing import Any

from bson import ObjectId
from cleanstack.exceptions import NotFoundError
from pymongo import ASCENDING

from app.domain.entities import EntityId
from app.domain.inventories.entities import Inventory, InventoryRecord, InventoryReport
from app.domain.protocols.repository import InventoryRepositoryProtocol
from app.infrastructure.repository.protocol import MongoRepositoryProtocol


class InventoryRepository(MongoRepositoryProtocol, InventoryRepositoryProtocol):
    def get_inventories(self) -> list[Inventory]:
        sort_keys = [("date", ASCENDING), ("shop", ASCENDING)]
        inventories = self.database["inventories"].find().sort(sort_keys)
        return [Inventory(**inventory) for inventory in inventories]

    def get_inventory(self, inventory_id: EntityId) -> Inventory | None:
        inventory = self.database["inventories"].find_one(
            {"_id": ObjectId(inventory_id)}
        )
        return Inventory(**inventory) if inventory else None

    def get_inventory_report(self, inventory_id: EntityId) -> InventoryReport | None:
        pipeline: list[dict[str, Any]] = [
            {"$match": {"_id": ObjectId(inventory_id)}},
            {
                "$lookup": {
                    "from": "inventory_records",
                    # convert ObjectId to string
                    "let": {"id_str": {"$toString": "$_id"}},
                    "pipeline": [
                        {"$match": {"$expr": {"$eq": ["$inventory_id", "$$id_str"]}}},
                        {
                            "$sort": {
                                "article_type": ASCENDING,
                                "article_name.name1": ASCENDING,
                                "article_name.name2": ASCENDING,
                            }
                        },
                    ],
                    "as": "records",
                }
            },
            {"$limit": 1},
        ]
        inventory = next(self.database["inventories"].aggregate(pipeline), None)
        return InventoryReport(**inventory) if inventory else None

    def create_inventory(self, inventory: Inventory) -> Inventory:
        result = self.database["inventories"].insert_one(
            inventory.model_dump(exclude={"id"})
        )
        inventory_db = self.database["inventories"].find_one(
            {"_id": result.inserted_id}
        )
        if not inventory_db:
            raise NotFoundError()

        return Inventory(**inventory_db)

    def create_inventory_records(
        self,
        inventory_id: EntityId,
        records: list[InventoryRecord],
    ) -> list[InventoryRecord]:
        self.database["inventory_records"].insert_many(
            [
                {
                    "inventory_id": inventory_id,
                    **record.model_dump(exclude={"inventory_id"}),
                }
                for record in records
            ]
        )

        records_db = self.database["inventory_records"].find(
            {"inventory_id": inventory_id}
        )
        return [InventoryRecord(**record) for record in records_db]

    def delete_inventory(self, inventory: Inventory) -> None:
        self.database["inventories"].delete_one({"_id": ObjectId(inventory.id)})

    def delete_inventory_records(self, inventory_id: EntityId) -> None:
        self.database["inventory_records"].delete_many(
            {"inventory_id": ObjectId(inventory_id)}
        )
