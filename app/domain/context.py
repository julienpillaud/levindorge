from typing import Protocol

from cleanstack.domain import UnitOfWorkProtocol

from app.domain.repository import RepositoryProtocol


class ContextProtocol(UnitOfWorkProtocol, Protocol):
    @property
    def repository(self) -> RepositoryProtocol: ...
