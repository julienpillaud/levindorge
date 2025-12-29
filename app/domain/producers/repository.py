from typing import Protocol

from app.domain.producers.entities import Producer, ProducerType
from app.domain.protocols.repository import RepositoryProtocol


class ProducerRepositoryProtocol(RepositoryProtocol[Producer], Protocol):
    def exists(self, name: str, producer_type: ProducerType) -> bool: ...
