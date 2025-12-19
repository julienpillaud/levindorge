from typing import Protocol

from app.domain._shared.protocols.repository import RepositoryProtocol
from app.domain.distributors.entities import Distributor


class DistributorRepositoryProtocol(RepositoryProtocol[Distributor], Protocol): ...
