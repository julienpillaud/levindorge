from typing import Literal

from pydantic import BaseModel

from app.domain.entities import DomainModel


class DepositCreate(BaseModel):
    category: Literal["Bière", "Fût", "Mini-fût"]
    deposit_type: Literal["Unitaire", "Caisse"]
    value: float


class Deposit(DomainModel):
    category: Literal["Bière", "Fût", "Mini-fût"]
    deposit_type: Literal["Unitaire", "Caisse"]
    value: float

    @property
    def name(self) -> str:
        return f"Consigne {self.category} {self.value:g} {self.deposit_type}"
