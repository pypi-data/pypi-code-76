from datetime import timedelta
from typing import NamedTuple


DEFAULT_REDIS_URL = "redis://localhost:6379/0"


class RateLimiterConfig(NamedTuple):
    limit: int
    time: timedelta
    redis_url: str = DEFAULT_REDIS_URL


class RateLimiterResponse(NamedTuple):
    remaining: int
    is_limited: bool
