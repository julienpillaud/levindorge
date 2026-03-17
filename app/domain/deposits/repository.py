from typing import Protocol

from cleanstack.domain import RepositoryProtocol

from app.domain.deposits.entities import Deposit


class DepositRepositoryProtocol(RepositoryProtocol[Deposit], Protocol):
    def create_many(self, deposits: list[Deposit]) -> list[Deposit]: ...

    def exists(self, deposit: Deposit, /) -> bool: ...
