import logfire

from app.api.app import create_fastapi_app
from app.core.config.settings import Settings
from app.core.logfire import scrubbing_callback

settings = Settings()
logfire.configure(
    send_to_logfire="if-token-present",
    token=settings.logfire_token,
    service_name="app",
    service_version=settings.app_version,
    environment=settings.environment,
    console=False,
    scrubbing=logfire.ScrubbingOptions(callback=scrubbing_callback),
)
# Should be before any pymongo import
logfire.instrument_pymongo(capture_statement=True)

logfire.instrument_redis(capture_statement=True)

app = create_fastapi_app(settings=settings)

logfire.instrument_fastapi(app, capture_headers=True, extra_spans=True)
