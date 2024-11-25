from fastapi import FastAPI

from app.config import settings

api = FastAPI(
    docs_url="/api/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url=None,
    openapi_url="/api/openapi.json" if settings.ENVIRONMENT == "development" else None,
    prefix="/api",
)


@api.get("/health")
async def health():
    return {"status": "ok"}
