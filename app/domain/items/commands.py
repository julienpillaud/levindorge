from app.domain.commons.entities import Item
from app.domain.context import ContextProtocol


def get_items_command(context: ContextProtocol, name: str) -> list[Item]:
    return context.repository.get_items(name=name)
