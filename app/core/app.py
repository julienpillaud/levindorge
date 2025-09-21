import logfire

from app.app.app import create_app
from app.core.config import Settings

settings = Settings()
logfire.configure(
    send_to_logfire="if-token-present",
    token=settings.logfire_token,
    service_name="app",
    service_version=settings.api_version,
    environment=settings.environment,
    console=False,
)
app = create_app(settings=settings)
logfire.instrument_fastapi(app, capture_headers=True, extra_spans=True)
logfire.instrument_pymongo(capture_statement=True)
