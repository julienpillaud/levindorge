from app.domain.context import ContextProtocol
from app.domain.entities import PaginatedResponse
from app.domain.volumes.entities import Volume, VolumeCategory


def get_volumes_command(
    context: ContextProtocol,
    volume_category: VolumeCategory | None = None,
) -> PaginatedResponse[Volume]:
    filters = {"category": volume_category} if volume_category else {}
    return context.volume_repository.get_all(
        filters=filters,
        sort={"category": 1, "normalized_value": 1},
        limit=300,
    )
