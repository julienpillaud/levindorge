from fastapi import FastAPI

api = FastAPI(
    openapi_url=None,
    root_path="/api",
)


@api.get("/health")
async def health():
    return {"status": "ok"}
