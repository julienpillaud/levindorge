from pydantic import BaseModel

from app.domain.articles.entities import Article
from app.domain.entities import EntityId
from app.domain.shops.entities import Shop


class POSArticleCreateOrUpdate(BaseModel):
    shop: Shop
    article: Article


class POSArticleDelete(BaseModel):
    shop: Shop
    article_id: EntityId
