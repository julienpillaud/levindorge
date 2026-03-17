from cleanstack.entities import Pagination
from rich import print

from app.core.context import Context
from app.domain.origins.entities import Origin
from data.origins import ORIGINS


def create_origins(dst_context: Context) -> list[Origin]:
    result = dst_context.origin_repository.create_many(ORIGINS)

    count = len(result)
    print(f"Created {count} origins")

    return dst_context.origin_repository.get_all(
        pagination=Pagination(page=1, size=count)
    ).items
