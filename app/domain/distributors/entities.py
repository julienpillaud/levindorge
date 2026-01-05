from app.domain.entities import DomainEntity


class Distributor(DomainEntity):
    name: str

    @property
    def display_name(self) -> str:
        return self.name
