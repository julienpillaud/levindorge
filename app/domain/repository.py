from typing import Protocol

from app.domain.articles.entities import Article
from app.domain.users.entities import User


class RepositoryProtocol(Protocol):
    def get_user_by_email(self, email: str) -> User | None: ...

    def get_articles_by_list_category(self, list_category: str) -> list[Article]: ...
