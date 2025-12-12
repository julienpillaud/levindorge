from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class AppPaths(BaseModel):
    root: Path = Path(__file__).resolve().parents[2]

    model_config = SettingsConfigDict(frozen=True)

    @property
    def static(self) -> Path:
        return self.root / "static"

    @property
    def templates(self) -> Path:
        return self.root / "templates"

    @property
    def price_labels(self) -> Path:
        path = self.templates / "price-labels-files"
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def fonts(self) -> Path:
        return self.static / "fonts"
