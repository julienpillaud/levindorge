from pathlib import Path

from fastapi.templating import Jinja2Templates

base_dir = Path(__file__).parents[2]
templates = Jinja2Templates(directory=base_dir / "app/application/templates")


def strip_zeros(value: float) -> str:
    return str(value).rstrip("0").rstrip(".")


templates.env.filters["strip_zeros"] = strip_zeros
