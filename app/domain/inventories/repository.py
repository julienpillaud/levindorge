from typing import Protocol

from app.domain.inventories.entities import Inventory
from app.domain.protocols.repository import RepositoryProtocol


class InventoryRepositoryProtocol(RepositoryProtocol[Inventory], Protocol): ...
