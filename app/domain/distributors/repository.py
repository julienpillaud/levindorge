from typing import Protocol

from cleanstack.domain import RepositoryProtocol

from app.domain.distributors.entities import Distributor


class DistributorRepositoryProtocol(RepositoryProtocol[Distributor], Protocol):
    def create_many(self, distributors: list[Distributor]) -> list[Distributor]: ...

    def get_by_name(self, name: str) -> Distributor | None: ...

    def exists(self, name: str) -> bool: ...
