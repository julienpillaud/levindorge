from typing import Annotated, Any

from fastapi import APIRouter, Depends

from app.api.auth.dependencies import get_current_user
from app.api.dependencies import get_domain
from app.domain.domain import Domain

router = APIRouter(prefix="/articles", tags=["Articles"])


@router.get("/", dependencies=[Depends(get_current_user)])
def get_articles(domain: Annotated[Domain, Depends(get_domain)]) -> Any:
    return domain.get_articles()


@router.get("/{article_id}", dependencies=[Depends(get_current_user)])
def get_article(
    domain: Annotated[Domain, Depends(get_domain)],
    article_id: str,
) -> Any:
    return domain.get_article(article_id=article_id)
