import json

import redis

from ..config import settings


redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)


def get_cache(
    key: str
):

    value = redis_client.get(key)

    if not value:
        return None

    return json.loads(value)


def set_cache(
    key: str,
    value,
    ttl=3600
):

    redis_client.setex(
        key,
        ttl,
        json.dumps(value)
    )