from typing import Protocol

from app.domain.producers.entities import Producer
from app.domain.protocols.repository import RepositoryProtocol


class ProducerRepositoryProtocol(RepositoryProtocol[Producer], Protocol):
    def exists(self, producer: Producer, /) -> bool: ...
