from typing import Protocol

from app.domain.origins.entities import Origin
from app.domain.protocols.repository import RepositoryProtocol


class OriginRepositoryProtocol(RepositoryProtocol[Origin], Protocol): ...
