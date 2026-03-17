from typing import Protocol

from cleanstack.domain import RepositoryProtocol

from app.domain.inventories.entities import Inventory, InventoryRecord


class InventoryRepositoryProtocol(RepositoryProtocol[Inventory], Protocol):
    def create_records(
        self,
        record: list[InventoryRecord],
    ) -> list[InventoryRecord]: ...
