from bson import ObjectId
from pymongo import ASCENDING, DESCENDING

from app.domain.items.entities import Deposit
from app.domain.protocols.repository import DepositRepositoryProtocol

DEPOSIT_TYPE_MAPPING = {"Unitaire": "unit", "Caisse": "case"}


class DepositRepository(DepositRepositoryProtocol):
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

    def get_deposit(self, deposit_id: str) -> Deposit | None:
        volume = self.database["deposits"].find_one({"_id": ObjectId(deposit_id)})
        return Deposit(**volume) if volume else None

    def delete_deposit(self, deposit: Deposit) -> None:
        self.database["deposits"].delete_one({"_id": ObjectId(deposit.id)})

    def deposit_is_used(self, deposit: Deposit) -> bool:
        deposit_key = DEPOSIT_TYPE_MAPPING[deposit.deposit_type]
        article = self.database["articles"].find_one(
            {f"deposit.{deposit_key}": deposit.value}
        )
        return article is not None
