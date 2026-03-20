from typing import Protocol

from cleanstack.domain import RepositoryProtocol

from app.domain.metadata.entities.deposits import Deposit
from app.domain.metadata.entities.distributors import Distributor
from app.domain.metadata.entities.origins import Origin
from app.domain.metadata.entities.producers import Producer
from app.domain.metadata.entities.volumes import Volume


class DepositRepositoryProtocol(RepositoryProtocol[Deposit], Protocol): ...


class DistributorRepositoryProtocol(RepositoryProtocol[Distributor], Protocol): ...


class OriginRepositoryProtocol(RepositoryProtocol[Origin], Protocol): ...


class ProducerRepositoryProtocol(RepositoryProtocol[Producer], Protocol): ...


class VolumeRepositoryProtocol(RepositoryProtocol[Volume], Protocol): ...
