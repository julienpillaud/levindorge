from typing import Protocol

from cleanstack.domain import RepositoryProtocol

from app.domain.metadata.entities.deposits import Deposit
from app.domain.metadata.entities.distributors import Distributor
from app.domain.metadata.entities.origins import Origin
from app.domain.metadata.entities.producers import Producer
from app.domain.metadata.entities.volumes import Volume


class DepositRepositoryProtocol(RepositoryProtocol[Deposit], Protocol): ...


class DistributorRepositoryProtocol(RepositoryProtocol[Distributor], Protocol):
    def get_by_name(self, name: str) -> Distributor | None: ...


class OriginRepositoryProtocol(RepositoryProtocol[Origin], Protocol):
    def get_by_name(self, name: str) -> Origin | None: ...


class ProducerRepositoryProtocol(RepositoryProtocol[Producer], Protocol):
    def get_by_name(self, name: str) -> Producer | None: ...


class VolumeRepositoryProtocol(RepositoryProtocol[Volume], Protocol): ...
