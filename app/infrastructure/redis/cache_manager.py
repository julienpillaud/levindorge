from typing import cast

from redis import Redis

from app.domain.protocols.cache_manager import CacheManagerProtocol


class RedisCacheManager(CacheManagerProtocol):
    def __init__(self, client: Redis):
        self.client = client

    def set(self, key: str, value: str, ttl: int = 3600) -> None:
        self.client.set(name=key, value=value, ex=ttl)

    def get(self, key: str) -> str | None:
        return cast(str | None, self.client.get(key))

    def flush(self) -> None:
        self.client.flushdb()
