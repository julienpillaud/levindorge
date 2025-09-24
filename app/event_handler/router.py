from typing import Annotated, Any

from faststream import Context
from faststream.redis import RedisRouter

from app.domain.domain import Domain

router = RedisRouter()


@router.subscriber("create.article")
def create_article(
    message: Any,
    domain: Annotated[Domain, Context()],
) -> None:
    shop, article = message["shop"], message["article"]
    domain.create_pos_article(shop=shop, article=article)


@router.subscriber("delete.article")
def delete_article(
    message: Any,
    domain: Annotated[Domain, Context],
) -> None:
    shop, article_id = message["shop"], message["article_id"]
    domain.delete_pos_article(shop=shop, article_id=article_id)
