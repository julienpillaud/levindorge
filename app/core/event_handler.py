from faststream import ContextRepo, FastStream
from faststream.redis import RedisBroker

from app.core.config import Settings
from app.core.core import Context
from app.domain.domain import Domain
from app.event_handler.router import router

settings = Settings()
app_context = Context(settings=settings)
domain = Domain(context=app_context)

broker = RedisBroker(str(settings.redis_dsn))
broker.include_router(router)
app = FastStream(broker)


@app.on_startup
async def set_context(context: ContextRepo) -> None:
    context.set_global("domain", domain)
