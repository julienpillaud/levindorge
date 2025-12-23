from app.domain.caching import cached_command
from app.domain.context import ContextProtocol
from app.domain.entities import PaginatedResponse
from app.domain.volumes.entities import Volume, VolumeCategory


@cached_command(response_model=PaginatedResponse[Volume], ttl=3600)
def get_volumes_command(
    context: ContextProtocol,
    /,
    category: VolumeCategory | None = None,
) -> PaginatedResponse[Volume]:
    filters = {"category": category} if category else {}
    return context.volume_repository.get_all(
        filters=filters,
        sort={"category": 1, "normalized_value": 1},
        limit=300,
    )
