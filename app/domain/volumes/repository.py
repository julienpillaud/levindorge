from typing import Protocol

from cleanstack.domain import RepositoryProtocol

from app.domain.volumes.entities import Volume


class VolumeRepositoryProtocol(RepositoryProtocol[Volume], Protocol):
    def create_many(self, volumes: list[Volume]) -> list[Volume]: ...

    def exists(self, volume: Volume, /) -> bool: ...
