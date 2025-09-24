from typing import Protocol

from cleanstack.domain import UnitOfWorkProtocol

from app.domain.protocols.event_publisher import EventPublisherProtocol
from app.domain.protocols.pos_manager import POSManagerProtocol
from app.domain.protocols.repository import RepositoryProtocol


class ContextProtocol(UnitOfWorkProtocol, Protocol):
    @property
    def repository(self) -> RepositoryProtocol: ...
    @property
    def pos_manager(self) -> POSManagerProtocol: ...
    @property
    def event_publisher(self) -> EventPublisherProtocol: ...
