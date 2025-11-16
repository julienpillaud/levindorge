from typing import Protocol

from app.domain.protocols.base_repository import RepositoryProtocol
from app.domain.stores.entities import Store


class StoreRepositoryProtocol(RepositoryProtocol[Store], Protocol): ...
