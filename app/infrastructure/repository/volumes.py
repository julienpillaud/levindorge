from bson import ObjectId
from pymongo import ASCENDING

from app.domain.entities import EntityId
from app.domain.items.entities import Volume
from app.domain.protocols.repository import VolumeRepositoryProtocol
from app.infrastructure.repository.protocol import MongoRepositoryProtocol


class VolumeRepository(MongoRepositoryProtocol, VolumeRepositoryProtocol):
    def get_volumes(self) -> list[Volume]:
        sort_keys = [("category", ASCENDING), ("value", ASCENDING)]
        return [
            Volume(**volume)
            for volume in self.database["volumes"].find().sort(sort_keys)
        ]

    def get_volume(self, volume_id: EntityId) -> Volume | None:
        volume = self.database["volumes"].find_one({"_id": ObjectId(volume_id)})
        return Volume(**volume) if volume else None

    def delete_volume(self, volume: Volume) -> None:
        self.database["volumes"].delete_one({"_id": ObjectId(volume.id)})

    def volume_is_used(self, volume: Volume) -> bool:
        types = self.database["types"].find({"volume_category": volume.category})
        type_names = [x["name"] for x in types]
        article = self.database["articles"].find_one(
            {"volume.value": volume.value, "type": {"$in": type_names}}
        )
        return article is not None
