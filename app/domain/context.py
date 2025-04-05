from typing import Protocol

from app.domain.repository import RepositoryProtocol


class ContextProtocol(Protocol):
    @property
    def repository(self) -> RepositoryProtocol: ...
