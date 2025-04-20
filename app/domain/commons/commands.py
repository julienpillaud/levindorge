from typing import Any

from app.domain.articles.entities import TypeInfos
from app.domain.context import ContextProtocol


def get_type_infos_command(
    context: ContextProtocol,
    list_category: str,
) -> list[TypeInfos]:
    return context.repository.get_type_infos_by_list_category(
        list_category=list_category
    )


def get_template_context_command(
    context: ContextProtocol,
    volume_category: str | None,
) -> dict[str, Any]:
    return context.repository.get_template_context(volume_category=volume_category)
