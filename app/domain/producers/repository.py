from typing import Protocol

from app.domain._shared.protocols.repository import RepositoryProtocol
from app.domain.producers.entities import Producer


class ProducerRepositoryProtocol(RepositoryProtocol[Producer], Protocol): ...
