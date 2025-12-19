from typing import Protocol

from app.domain._shared.protocols.repository import RepositoryProtocol
from app.domain.inventories.entities import Inventory


class InventoryRepositoryProtocol(RepositoryProtocol[Inventory], Protocol): ...
