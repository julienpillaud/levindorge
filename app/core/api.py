import logfire

from app.api.api import create_api
from app.core.config import Settings
from app.core.core import initialize_app

settings = Settings()
logfire.configure(
    send_to_logfire="if-token-present",
    token=settings.logfire_token,
    service_name="api",
    service_version=settings.api_version,
    environment=settings.environment,
    console=False,
)
api = create_api(settings=settings)
initialize_app(settings=settings, app=api)
logfire.instrument_fastapi(api, capture_headers=True, extra_spans=True)
logfire.instrument_pymongo(capture_statement=True)
