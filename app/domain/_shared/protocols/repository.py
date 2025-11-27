from typing import Protocol

from app.domain.entities import EntityId
from app.domain.inventories.entities import Inventory, InventoryRecord, InventoryReport


class InventoryRepositoryProtocol(Protocol):
    def get_inventories(self) -> list[Inventory]: ...

    def get_inventory(self, inventory_id: EntityId) -> Inventory | None: ...

    def get_inventory_report(
        self,
        inventory_id: EntityId,
    ) -> InventoryReport | None: ...

    def create_inventory(self, inventory: Inventory) -> Inventory: ...

    def create_inventory_records(
        self,
        inventory_id: EntityId,
        records: list[InventoryRecord],
    ) -> list[InventoryRecord]: ...

    def delete_inventory(self, inventory: Inventory) -> None: ...

    def delete_inventory_records(self, inventory_id: EntityId) -> None: ...


class RepositoryProtocol(InventoryRepositoryProtocol, Protocol): ...
