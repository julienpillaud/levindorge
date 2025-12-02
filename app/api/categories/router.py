from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.auth.dependencies import get_current_user
from app.api.dependencies import get_domain
from app.domain.categories.entities import Category
from app.domain.domain import Domain

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", dependencies=[Depends(get_current_user)])
def get_categories(domain: Annotated[Domain, Depends(get_domain)]) -> list[Category]:
    categories = domain.get_categories()
    return categories.items
