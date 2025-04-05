from typing import Annotated, Any

from fastapi import APIRouter, Depends

from app.api.auth.dependencies import get_current_user
from app.api.dependencies import get_domain
from app.domain.domain import Domain
from app.domain.users.entities import User

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("")
async def get_articles(
    current_user: Annotated[User, Depends(get_current_user)],
    domain: Annotated[Domain, Depends(get_domain)],
) -> Any:
    return {"message": "List of articles"}
