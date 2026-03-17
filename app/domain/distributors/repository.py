from typing import Protocol

from cleanstack.domain import RepositoryProtocol

from app.domain.distributors.entities import Distributor


class DistributorRepositoryProtocol(RepositoryProtocol[Distributor], Protocol):
    def create_many(self, distributors: list[Distributor]) -> list[Distributor]: ...

    def exists(self, name: str) -> bool: ...
