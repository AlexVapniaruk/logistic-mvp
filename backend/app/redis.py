import os
import redis.asyncio as aioredis
from typing import AsyncIterator

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

_client: aioredis.Redis | None = None


async def init_redis() -> None:
    global _client
    _client = aioredis.from_url(REDIS_URL, decode_responses=True)


async def close_redis() -> None:
    if _client:
        await _client.aclose()


def get_redis() -> aioredis.Redis:
    if _client is None:
        raise RuntimeError("Redis not initialised")
    return _client


async def publish(channel: str, message: str) -> None:
    await get_redis().publish(channel, message)


async def subscribe(channel: str) -> AsyncIterator[str]:
    pubsub = get_redis().pubsub()
    await pubsub.subscribe(channel)
    async for msg in pubsub.listen():
        if msg["type"] == "message":
            yield msg["data"]
