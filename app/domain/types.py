from decimal import Decimal
from typing import Annotated

from pydantic import PlainSerializer

type EntityId = str
type StoreSlug = str
DecimalType = Annotated[Decimal, PlainSerializer(str)]
