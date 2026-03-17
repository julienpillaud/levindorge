from typing import Protocol

from cleanstack.domain import RepositoryProtocol

from app.domain.origins.entities import Origin


class OriginRepositoryProtocol(RepositoryProtocol[Origin], Protocol):
    def create_many(self, origins: list[Origin]) -> list[Origin]: ...

    def exists(self, origin: Origin) -> bool: ...
