from typing import Protocol

from app.domain.price_labels.entities import PriceLabelSheet
from app.domain.protocols.repository import RepositoryProtocol


class PriceLabelRepositoryProtocol(RepositoryProtocol[PriceLabelSheet], Protocol): ...
