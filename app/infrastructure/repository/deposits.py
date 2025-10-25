from bson import ObjectId
from cleanstack.exceptions import NotFoundError
from pymongo import ASCENDING, DESCENDING

from app.domain.deposits.entities import Deposit
from app.domain.entities import EntityId
from app.domain.protocols.repository import DepositRepositoryProtocol
from app.infrastructure.repository.protocol import MongoRepositoryProtocol

DEPOSIT_TYPE_MAPPING = {"Unitaire": "unit", "Caisse": "case"}


class DepositRepository(MongoRepositoryProtocol, DepositRepositoryProtocol):
    def get_deposits(self) -> list[Deposit]:
        sort_keys = [
            ("category", ASCENDING),
            ("deposit_type", DESCENDING),
            ("value", ASCENDING),
        ]
        return [
            Deposit(**deposit)
            for deposit in self.database["deposits"].find().sort(sort_keys)
        ]

    def get_deposit(self, deposit_id: EntityId) -> Deposit | None:
        deposit = self.database["deposits"].find_one({"_id": ObjectId(deposit_id)})
        return Deposit(**deposit) if deposit else None

    def deposit_exists(self, deposit: Deposit) -> bool:
        result = self.database["deposits"].find_one(
            {
                "category": deposit.category,
                "deposit_type": deposit.deposit_type,
                "value": deposit.value,
            }
        )
        return result is not None

    def create_deposit(self, deposit: Deposit) -> Deposit:
        result = self.database["deposits"].insert_one(
            deposit.model_dump(exclude={"id"})
        )
        return self._get_deposit_by_id(volume_id=result.inserted_id)

    def delete_deposit(self, deposit: Deposit) -> None:
        self.database["deposits"].delete_one({"_id": ObjectId(deposit.id)})

    def deposit_is_used(self, deposit: Deposit) -> bool:
        deposit_key = DEPOSIT_TYPE_MAPPING[deposit.deposit_type]
        article = self.database["articles"].find_one(
            {f"deposit.{deposit_key}": deposit.value}
        )
        return article is not None

    def _get_deposit_by_id(self, volume_id: EntityId) -> Deposit:
        deposit = self.database["deposits"].find_one({"_id": ObjectId(volume_id)})
        if not deposit:
            raise NotFoundError()

        return Deposit(**deposit)
