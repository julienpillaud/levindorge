from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/application/templates")


def strip_zeros(value: float) -> str:
    return str(value).rstrip("0").rstrip(".")


templates.env.filters["strip_zeros"] = strip_zeros
