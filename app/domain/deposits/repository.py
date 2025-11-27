from typing import Protocol

from app.domain._shared.protocols.base_repository import RepositoryProtocol
from app.domain.deposits.entities import Deposit


class DepositRepositoryProtocol(RepositoryProtocol[Deposit], Protocol): ...
