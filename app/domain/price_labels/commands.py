from operator import attrgetter

from app.core.config.settings import Settings
from app.domain.context import ContextProtocol
from app.domain.price_labels.entities import (
    PriceLabelCreate,
    PriceLabelFile,
)
from app.domain.price_labels.utils.common import split_by_size
from app.domain.price_labels.utils.large import create_large_price_labels
from app.domain.price_labels.utils.small import create_small_price_labels
from app.domain.stores.entities import Store


def create_price_labels_command(
    context: ContextProtocol,
    settings: Settings,
    current_store: Store,
    price_labels_create: list[PriceLabelCreate],
) -> None:
    large_price_labels, small_price_labels = split_by_size(
        context=context,
        price_labels=price_labels_create,
    )
    if large_price_labels:
        create_large_price_labels(
            context=context,
            settings=settings,
            current_store=current_store,
            price_labels=large_price_labels,
        )
    if small_price_labels:
        create_small_price_labels(
            settings=settings,
            current_store=current_store,
            price_labels=small_price_labels,
        )


def get_price_labels_files_command(
    context: ContextProtocol,
    settings: Settings,
) -> list[PriceLabelFile]:
    files = [
        PriceLabelFile.from_path(file)
        for file in settings.app_path.price_labels.glob("*.html")
    ]
    files = sorted(files, key=attrgetter("date", "id"))
    return files
