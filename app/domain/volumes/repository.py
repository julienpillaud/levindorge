from typing import Protocol

from app.domain.protocols.repository import RepositoryProtocol
from app.domain.volumes.entities import Volume


class VolumeRepositoryProtocol(RepositoryProtocol[Volume], Protocol):
    def exists(self, volume: Volume, /) -> bool: ...
