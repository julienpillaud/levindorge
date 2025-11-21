from typing import Protocol

from app.domain._shared.protocols.base_repository import RepositoryProtocol
from app.domain.producers.entities import Producer


class ProducerRepositoryProtocol(RepositoryProtocol[Producer], Protocol): ...
