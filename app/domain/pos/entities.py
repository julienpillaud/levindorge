import datetime

from pydantic import BaseModel

from app.domain.articles.entities import Article
from app.domain.entities import EntityId
from app.domain.stores.entities import Store


class POSArticleCreateOrUpdate(BaseModel):
    store: Store
    article: Article


class POSArticleDelete(BaseModel):
    store: Store
    article_id: EntityId


class POSArticle(BaseModel):
    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    stock_quantity: int = 0
    category_id: str
    name: str
    reference: str
