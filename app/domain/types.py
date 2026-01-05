from collections.abc import Callable
from decimal import Decimal
from typing import Annotated, Concatenate

from pydantic import BaseModel, PlainSerializer

from app.domain.context import ContextProtocol

type Command[**P, R: BaseModel] = Callable[Concatenate[ContextProtocol, P], R]

type StoreName = str
type StoreSlug = str
DecimalType = Annotated[Decimal, PlainSerializer(float)]
