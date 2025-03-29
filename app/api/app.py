# pyright: reportUnusedFunction=false
from fastapi import FastAPI

from app.domain.domain import Domain


def app_factory(domain: Domain) -> FastAPI:
    app = FastAPI(
        openapi_url=None,
        root_path="/api",
    )

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app
