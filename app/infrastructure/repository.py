from copy import deepcopy
from typing import Any, TypeVar

from pymongo.database import Database

from app.domain.entities import DomainModel
from app.domain.repository import RepositoryProtocol
from app.domain.users.entities import User

T = TypeVar("T", bound=DomainModel)


class MongoRepository(RepositoryProtocol):
    def __init__(self, database: Database[dict[str, Any]]):
        self.database = database

    @staticmethod
    def _to_domain(db_entity: dict[str, Any], entity_type: type[T]) -> T:
        data = deepcopy(db_entity)
        entity_id = str(data.pop("_id"))
        return entity_type(id=entity_id, **data)

    def get_user_by_email(self, email: str) -> User | None:
        user = self.database.users.find_one({"email": email})
        return self._to_domain(user, User) if user else None
