from typing import cast

from redis import Redis

from app.domain.protocols.cache_manager import CacheManagerProtocol


class RedisCacheManager(CacheManagerProtocol):
    def __init__(self, client: Redis):
        self.client = client

    def set(
        self,
        key: str,
        value: str,
        ttl: int = 3600,
        tag: str | None = None,
    ) -> None:
        self.client.set(name=key, value=value, ex=ttl)

        if tag:
            tag_key = f"tag:{tag}"
            self.client.sadd(tag_key, key)
            self.client.expire(tag_key, ttl)

    def get(self, key: str) -> str | None:
        return cast(str | None, self.client.get(key))

    def invalidate_tag(self, tag: str) -> None:
        tag_key = f"tag:{tag}"
        keys_to_delete = self.client.smembers(tag_key)

        if keys_to_delete:
            self.client.delete(*keys_to_delete, tag_key)

    def flush(self) -> None:
        self.client.flushdb()
