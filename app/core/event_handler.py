import logfire
from faststream import ContextRepo, FastStream
from faststream.redis import RedisBroker
from faststream.redis.opentelemetry import RedisTelemetryMiddleware

from app.core.config.settings import Settings
from app.core.core import Context
from app.core.logfire import scrubbing_callback
from app.domain.domain import Domain
from app.event_handler.router import router

settings = Settings()
logfire.configure(
    send_to_logfire="if-token-present",
    token=settings.logfire_token,
    service_name="worker",
    service_version=settings.app_version,
    environment=settings.environment,
    console=False,
    scrubbing=logfire.ScrubbingOptions(callback=scrubbing_callback),
)
logfire.instrument_pymongo(capture_statement=True)

app_context = Context(settings=settings)
domain = Domain(context=app_context)

broker = RedisBroker(
    str(settings.redis_dsn),
    middlewares=(RedisTelemetryMiddleware(),),
)
broker.include_router(router)
app = FastStream(broker)


@app.on_startup
async def set_context(context: ContextRepo) -> None:
    context.set_global("domain", domain)
