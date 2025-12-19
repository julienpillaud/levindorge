from typing import Protocol

from app.domain._shared.protocols.repository import RepositoryProtocol
from app.domain.origins.entities import Origin


class OriginRepositoryProtocol(RepositoryProtocol[Origin], Protocol): ...
