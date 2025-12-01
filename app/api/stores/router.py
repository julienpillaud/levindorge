from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.auth.dependencies import get_current_user
from app.api.dependencies import get_domain
from app.api.stores.dtos import StoreDTO
from app.domain.domain import Domain

router = APIRouter(prefix="/stores", tags=["Stores"])


@router.get("", dependencies=[Depends(get_current_user)])
def get_stores(domain: Annotated[Domain, Depends(get_domain)]) -> list[StoreDTO]:
    stores = domain.get_stores()
    return stores.items
