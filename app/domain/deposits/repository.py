from typing import Protocol

from app.domain._shared.protocols.repository import RepositoryProtocol
from app.domain.deposits.entities import Deposit


class DepositRepositoryProtocol(RepositoryProtocol[Deposit], Protocol): ...
