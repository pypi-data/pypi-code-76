import logging
from datetime import timedelta
from typing import List, Optional, Tuple

from redis import Redis, RedisError

from garm_rate_limiter.config import RateLimiterConfig, RateLimiterResponse
from garm_rate_limiter.constants import RATE_LIMIT_KEY_TEMPLATE_PREFIX
from garm_rate_limiter.exceptions import (
    RateLimiterConfigValidationError,
    RateLimiterException,
    RateLimitExceeded,
)


logger = logging.getLogger(__name__)


class SingletonMeta(type):
    """Singleton metaclass. Referenced from: https://stackoverflow.com/a/6798042/2972179"""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class RateLimiter(metaclass=SingletonMeta):
    def __init__(self, redis_url: str):
        try:
            self.redis_client = Redis.from_url(redis_url)
        except RedisError as e:
            raise RateLimiterException(
                "An error occurred while establishing connection with Redis."
            ) from e

    def check_rate_limit(
        self, config: RateLimiterConfig, key: str
    ) -> RateLimiterResponse:
        try:
            # Retrieve current rate from Redis
            current_rate = self.redis_client.get(key)
            # If current rate exists
            if current_rate is not None:
                # Decode current rate from UTF-8 and convert to integer
                current_rate = int(current_rate.decode(encoding="utf-8"))
                if current_rate >= config.limit:
                    return RateLimiterResponse(
                        remaining=0,
                        is_limited=True,
                    )

            # If no rate limiting has happened, then increment the current rate.
            # Redis will set the current rate as 1 if it does not exist.
            value = self.redis_client.incr(key)
            # If the key has been just set
            if value == 1:
                # Set an expire flag for the key.
                self.redis_client.expire(
                    key,
                    config.time,
                )

            return RateLimiterResponse(
                remaining=config.limit - value, is_limited=False
            )
        except RedisError as e:
            raise RateLimiterException(
                "An error occurred while handling the rate limit check."
            ) from e


class RateLimiterMiddleware:
    def __init__(self, config: RateLimiterConfig, app):
        self.config = self.validate_config(config)
        self.app = app

    @staticmethod
    def validate_config(config):
        if not isinstance(config, RateLimiterConfig):
            raise RateLimiterConfigValidationError(
                "Invalid RateLimiterConfig."
            )

        if not isinstance(config.limit, int):
            raise RateLimiterConfigValidationError(
                "Invalid limit value in RateLimiterConfig. It must be an integer value."
            )

        if not isinstance(config.time, timedelta):
            raise RateLimiterConfigValidationError(
                "Invalid time value in RateLimiterConfig. It must be a timedelta value."
            )

        if not isinstance(config.redis_url, str):
            raise RateLimiterConfigValidationError(
                "Invalid redis_url value in RateLimiterConfig. It must be a string value."
            )

        return config

    @staticmethod
    def get_ip_address(environment):
        if "HTTP_X_FORWARDED_FOR" in environment:
            return environment["HTTP_X_FORWARDED_FOR"]
        return environment.get("REMOTE_ADDR", "127.0.0.1")

    def __call__(self, environment, start_response):
        ip_address = self.get_ip_address(environment)

        # If the IP address was not found
        if ip_address is None:
            logger.warning("No IP address found for the request.")
            return self.app(environment, start_response)

        rate_limit_response: Optional[RateLimiterResponse] = None
        try:
            limiter = RateLimiter(redis_url=self.config.redis_url)
            key = RATE_LIMIT_KEY_TEMPLATE_PREFIX.format(
                endpoint=environment["REQUEST_URI"],
                ip_address=ip_address,
                time=self.config.time.total_seconds(),
            )
            rate_limit_response = limiter.check_rate_limit(
                config=self.config, key=key
            )
        except RateLimiterException:
            # If an error has occurred we log it and do not do any rate limiting.
            logger.exception("An error occurred while checking rate limit.")

        if rate_limit_response is not None:

            def inject_rate_limit_headers(
                status: str,
                headers: List[Tuple[str, str]],
                exc_info=None,
            ):
                headers.extend(
                    [
                        ("X-RateLimit-Limit", str(self.config.limit)),
                        (
                            "X-RateLimit-Remaining",
                            str(rate_limit_response.remaining),
                        ),
                    ]
                )
                return start_response(status, headers, exc_info)

            if rate_limit_response.is_limited:
                return RateLimitExceeded()(
                    environment, inject_rate_limit_headers
                )
            return self.app(environment, inject_rate_limit_headers)

        return self.app(environment, start_response)
