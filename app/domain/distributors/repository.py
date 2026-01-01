from typing import Protocol

from app.domain.distributors.entities import Distributor
from app.domain.protocols.repository import RepositoryProtocol


class DistributorRepositoryProtocol(RepositoryProtocol[Distributor], Protocol):
    def exists(self, name: str) -> bool: ...
