import pytest

from app.core.config import Settings

pytest_plugins = [
    "tests.fixtures.database",
    "tests.fixtures.factories",
    "tests.fixtures.repositories",
]


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings(
        mongo_user="user",
        mongo_password="password",
        mongo_host="localhost",
        mongo_port=27017,
        mongo_database="test",
    )
