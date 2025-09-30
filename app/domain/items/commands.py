from collections.abc import Sequence

from app.domain.context import ContextProtocol
from app.domain.items.entities import Deposit, Item, ItemName, Volume


def get_items_command(
    context: ContextProtocol,
    name: str,
) -> Sequence[Item | Volume | Deposit]:
    match name:
        case (
            ItemName.BREWERIES
            | ItemName.DISTILLERIES
            | ItemName.DISTRIBUTORS
            | ItemName.COUNTRIES
            | ItemName.REGIONS
        ):
            return context.repository.get_items(name=name)
        case ItemName.VOLUMES:
            return context.repository.get_volumes()
        case ItemName.DEPOSITS:
            return context.repository.get_deposits()
        case _:
            raise ValueError()
