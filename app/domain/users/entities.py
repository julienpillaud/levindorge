from app.domain.entities import DomainModel
from app.domain.shops.entities import Shop


class User(DomainModel):
    name: str
    username: str
    email: str
    hashed_password: str
    shops: list[Shop]
