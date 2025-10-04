from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

EntityId = Annotated[str, BeforeValidator(str)]


class DomainModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: EntityId = Field(alias="_id")
