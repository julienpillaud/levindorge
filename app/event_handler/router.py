import logging
from collections.abc import Callable
from typing import Annotated, ParamSpec, TypeVar

import logfire
from faststream import Context
from faststream.rabbit import RabbitRouter
from tactill import TactillError
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential_jitter,
)

from app.domain.domain import Domain
from app.domain.exceptions import POSManagerError
from app.domain.pos.entities import POSArticleRequest

logger = logging.getLogger(__name__)

P = ParamSpec("P")
R = TypeVar("R")

router = RabbitRouter()


@router.subscriber("create.article")
def create_article(
    message: POSArticleRequest,
    domain: Annotated[Domain, Context()],
) -> None:
    logfire.info(
        f"Creating article for {message.store.name}",
        extra=message.model_dump(),
    )
    retry_command(domain.create_pos_article, data=message)


@router.subscriber("update.article")
def update_article(
    message: POSArticleRequest,
    domain: Annotated[Domain, Context()],
) -> None:
    logfire.info(
        f"Updating article for {message.store.name}",
        extra=message.model_dump(),
    )
    retry_command(domain.update_pos_article, data=message)


@router.subscriber("delete.article")
def delete_article(
    message: POSArticleRequest,
    domain: Annotated[Domain, Context()],
) -> None:
    logfire.info(
        f"Deleting article for {message.store.name}",
        extra=message.model_dump(),
    )
    retry_command(domain.delete_pos_article, data=message)


@retry(
    retry=(
        retry_if_exception_type(POSManagerError) | retry_if_exception_type(TactillError)
    ),
    wait=wait_exponential_jitter(),
    stop=stop_after_attempt(5),
    reraise=True,
    before_sleep=before_sleep_log(logger, logging.WARNING),
)
def retry_command(
    func: Callable[P, R],
    *args: P.args,
    **kwargs: P.kwargs,
) -> R:
    return func(*args, **kwargs)
