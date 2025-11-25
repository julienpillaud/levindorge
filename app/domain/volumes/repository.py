from typing import Protocol

from app.domain._shared.protocols.base_repository import RepositoryProtocol
from app.domain.volumes.entities import Volume


class VolumeRepositoryProtocol(RepositoryProtocol[Volume], Protocol): ...
