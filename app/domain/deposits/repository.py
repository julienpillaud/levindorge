from typing import Protocol

from app.domain.deposits.entities import Deposit
from app.domain.protocols.repository import RepositoryProtocol


class DepositRepositoryProtocol(RepositoryProtocol[Deposit], Protocol):
    def exists(self, deposit: Deposit, /) -> bool: ...
