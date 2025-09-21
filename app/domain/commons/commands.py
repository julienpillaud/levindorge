from app.domain.commons.entities import DisplayGroup, ViewData
from app.domain.context import ContextProtocol


def get_view_data_command(
    context: ContextProtocol,
    name: str | None = None,
    display_group: DisplayGroup | None = None,
) -> ViewData:
    article_types = context.repository.get_article_types(
        name=name,
        display_group=display_group,
    )
    article_type = article_types[0]
    items = context.repository.get_items_dict(
        volume_category=article_type.volume_category
    )
    return ViewData(
        display_group=article_type.display_group,
        pricing_group=article_type.pricing_group,
        article_type_names=[x.name for x in article_types],
        items=items,
    )
