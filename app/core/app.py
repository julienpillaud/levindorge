from fastapi import FastAPI

from app.api.articles.router import router as articles_router
from app.api.auth.router import router as auth_router
from app.api.utils import add_exceptions_handler, add_session_middleware, mount_static

app = FastAPI(openapi_url=None, root_path="/api")
add_session_middleware(app=app)
add_exceptions_handler(app=app)
mount_static(app=app)

app.include_router(articles_router)
app.include_router(auth_router)
