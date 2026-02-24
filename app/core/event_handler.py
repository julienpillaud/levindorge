import logfire

from app.core.config.settings import Settings
from app.core.logfire import scrubbing_callback
from app.event_handler.app import create_faststream_app

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

app = create_faststream_app(settings=settings)
