from pydantic import BaseModel, ConfigDict, Field
from tactill import TactillClient

from app.domain.entities import EntityId

type ArticleReference = str


class POSArticleContainer(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    client: TactillClient = Field(repr=False)
    article_id: EntityId
    name: str
    stock_quantity: int


class Container(BaseModel):
    reference: ArticleReference
    in_dashboard: bool
    pos: list[POSArticleContainer]

    @property
    def empty_stock(self) -> bool:
        return all(x.stock_quantity <= 0 for x in self.pos)


class Containers(BaseModel):
    containers: list[Container]

    @property
    def total(self) -> int:
        return len(self.containers)

    @property
    def only_in_dashboard(self) -> int:
        return sum(bool(c.in_dashboard and not c.pos) for c in self.containers)

    @property
    def only_in_pos(self) -> int:
        return sum(bool(c.pos and not c.in_dashboard) for c in self.containers)

    @property
    def in_both(self) -> int:
        return sum(bool(c.in_dashboard and c.pos) for c in self.containers)

    @property
    def in_pos_with_stock(self) -> int:
        return sum(bool(c.pos and not c.empty_stock) for c in self.containers)

    @property
    def in_both_with_stock(self) -> int:
        return sum(
            bool(c.in_dashboard and c.pos and not c.empty_stock)
            for c in self.containers
        )

    @property
    def only_in_pos_with_stock(self) -> int:
        return sum(
            bool(c.pos and not c.empty_stock and not c.in_dashboard)
            for c in self.containers
        )
