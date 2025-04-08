from typing import Annotated, Any

from fastapi import APIRouter, Depends
from fastapi.requests import Request

from app.api.auth.dependencies import get_current_user
from app.api.dependencies import get_domain
from app.core.templates import templates
from app.domain.domain import Domain
from app.domain.users.entities import User

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("/{list_category}")
async def get_articles(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    domain: Annotated[Domain, Depends(get_domain)],
    list_category: str,
) -> Any:
    articles = domain.get_articles(list_category=list_category)
    return templates.TemplateResponse(
        request=request,
        name="articles.html",
        context={"current_user": current_user, "articles": articles},
    )
