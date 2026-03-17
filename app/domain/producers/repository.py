from typing import Protocol

from cleanstack.domain import RepositoryProtocol

from app.domain.producers.entities import Producer


class ProducerRepositoryProtocol(RepositoryProtocol[Producer], Protocol):
    def create_many(self, producers: list[Producer]) -> list[Producer]: ...

    def get_by_name(self, name: str) -> Producer | None: ...

    def exists(self, producer: Producer, /) -> bool: ...
