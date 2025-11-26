from typing import Protocol

from app.domain._shared.protocols.base_repository import RepositoryProtocol
from app.domain.distributors.entities import Distributor


class DistributorRepositoryProtocol(RepositoryProtocol[Distributor], Protocol): ...
