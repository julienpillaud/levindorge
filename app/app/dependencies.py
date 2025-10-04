from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from fastapi.templating import Jinja2Templates

from app.api.dependencies import get_settings
from app.app.utils import init_templates
from app.core.config import Settings


@lru_cache(maxsize=1)
def get_templates(
    settings: Annotated[Settings, Depends(get_settings)],
) -> Jinja2Templates:
    return init_templates(settings=settings)
