from typing import Protocol

from app.domain._shared.protocols.repository import RepositoryProtocol
from app.domain.price_labels.entities import PriceLabelSheet


class PriceLabelRepositoryProtocol(RepositoryProtocol[PriceLabelSheet], Protocol): ...
