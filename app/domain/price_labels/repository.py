from typing import Protocol

from cleanstack.domain import RepositoryProtocol

from app.domain.price_labels.entities import PriceLabelSheet


class PriceLabelRepositoryProtocol(RepositoryProtocol[PriceLabelSheet], Protocol):
    def create_many(
        self,
        price_labels: list[PriceLabelSheet],
    ) -> list[PriceLabelSheet]: ...
