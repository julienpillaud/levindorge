from typing import Annotated, Any

from fastapi import APIRouter, Depends
from fastapi.requests import Request

from app.api.auth.dependencies import get_current_shop, get_current_user
from app.api.dependencies import get_domain
from app.api.templates import templates
from app.domain.domain import Domain
from app.domain.shops.entities import Shop
from app.domain.users.entities import User

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("/{list_category}")
async def get_articles(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    current_shop: Annotated[Shop, Depends(get_current_shop)],
    domain: Annotated[Domain, Depends(get_domain)],
    list_category: str,
) -> Any:
    articles = domain.get_articles(
        current_shop=current_shop,
        list_category=list_category,
    )

    return templates.TemplateResponse(
        request=request,
        name="article_list.html",
        context={
            "current_user": current_user,
            "current_shop": current_shop,
            "articles": articles,
            "list_category": list_category,
        },
    )


@router.get("/{article_id}/update")
async def update_article_view():
    return {}


@router.get("/{article_id}/delete")
async def delete_article():
    return {}
