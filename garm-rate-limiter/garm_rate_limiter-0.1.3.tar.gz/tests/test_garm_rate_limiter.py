"""Tests for `garm_rate_limiter` package."""
from contextlib import contextmanager
from datetime import timedelta
from unittest.mock import patch

import pytest
import redis
from pkg_resources import parse_version
from werkzeug import Client
from werkzeug.testapp import test_app as werkzeug_test_app
from werkzeug.wrappers import BaseResponse

import garm_rate_limiter
from garm_rate_limiter.config import DEFAULT_REDIS_URL, RateLimiterConfig
from garm_rate_limiter.exceptions import RateLimiterConfigValidationError
from garm_rate_limiter.limiter import RateLimiter, RateLimiterMiddleware


@contextmanager
def not_raises(expected_exception):
    try:
        yield

    except expected_exception as error:
        raise AssertionError(f"Raised exception {error} when it should not!")

    except Exception as error:
        raise AssertionError(f"An unexpected exception {error} raised.")


def test_valid_version():
    """Check that the package defines a valid ``__version__``."""
    v_curr = parse_version(garm_rate_limiter.__version__)
    v_orig = parse_version("0.1.0-dev")
    assert v_curr >= v_orig


def test_rate_limit_singleton():
    limiter_1 = RateLimiter(redis_url=DEFAULT_REDIS_URL)
    limiter_2 = RateLimiter(redis_url=DEFAULT_REDIS_URL)
    limiter_3 = RateLimiter(redis_url=DEFAULT_REDIS_URL)

    assert id(limiter_1) == id(limiter_2) == id(limiter_3)


def test_rate_limiter_config():
    config = RateLimiterConfig(limit=5, time=timedelta(seconds=32))
    assert config.limit == 5
    assert config.time == timedelta(seconds=32)

    config = RateLimiterConfig(limit=99, time=timedelta(hours=1))
    assert config.limit == 99
    assert config.time == timedelta(hours=1)


def test_rate_limiter_config_validation():
    # Test config validation
    with pytest.raises(RateLimiterConfigValidationError):
        config = RateLimiterConfig(limit=99, time=1)
        RateLimiterMiddleware.validate_config(config)

    with pytest.raises(RateLimiterConfigValidationError):
        config = RateLimiterConfig(limit="99", time=timedelta(hours=1))
        RateLimiterMiddleware.validate_config(config)

    with pytest.raises(RateLimiterConfigValidationError):
        RateLimiterMiddleware.validate_config(None)

    with pytest.raises(RateLimiterConfigValidationError):
        config = RateLimiterConfig(
            limit=1, time=timedelta(hours=1), redis_url=None
        )
        RateLimiterMiddleware.validate_config(config)

    # Valid config
    with not_raises(RateLimiterConfigValidationError):
        config = RateLimiterConfig(
            limit=1,
            time=timedelta(hours=1),
            redis_url="redis://localhost:6379/0",
        )
        RateLimiterMiddleware.validate_config(config)


def test_get_ip_address():
    """
    If HTTP_X_FORWARDED_FOR exists, we will return that, otherwise REMOTE_ADDR.
    If both do not exist, we will return localhost as fallback.
    """
    assert (
        RateLimiterMiddleware.get_ip_address(
            {
                "HTTP_X_FORWARDED_FOR": "192.168.1.5",
                "REMOTE_ADDR": "192.168.1.6",
            }
        )
        == "192.168.1.5"
    )

    assert (
        RateLimiterMiddleware.get_ip_address(
            {"HTTP_X_FORWARDED_FOR": "192.168.1.7"}
        )
        == "192.168.1.7"
    )

    assert (
        RateLimiterMiddleware.get_ip_address({"REMOTE_ADDR": "192.168.1.8"})
        == "192.168.1.8"
    )

    assert RateLimiterMiddleware.get_ip_address({}) == "127.0.0.1"


def test_rate_limiter():
    with patch.object(
        RateLimiterMiddleware, "get_ip_address", return_value="192.168.1.1"
    ):
        config = RateLimiterConfig(limit=10, time=timedelta(seconds=10))
        client = Client(
            RateLimiterMiddleware(app=werkzeug_test_app, config=config),
            BaseResponse,
        )

        # Make 10 requests without any rate limits
        for i in range(1, 11):
            response = client.get("/")
            assert response.status_code == 200
            # Check rate limit headers
            assert response.headers["X-RateLimit-Limit"] == "10"
            assert response.headers["X-RateLimit-Remaining"] == str(10 - i)

        # 11. request will not pass the rate limiter
        response = client.get("/")
        # The status code is 403
        assert response.status_code == 403
        assert response.headers["X-RateLimit-Limit"] == "10"
        assert response.headers["X-RateLimit-Remaining"] == "0"

        # Test another endpoint and make sure that rate limiting does not happen
        response = client.get("/user")
        # The status code is 403
        assert response.status_code == 200
        assert response.headers["X-RateLimit-Limit"] == "10"
        assert response.headers["X-RateLimit-Remaining"] == "9"

        # Flush Redis and make sure that requests won`t be rate limited
        redis_client = redis.Redis()
        redis_client.flushdb()

        response = client.get("/")
        assert response.status_code == 200
        assert response.headers["X-RateLimit-Limit"] == "10"
        assert response.headers["X-RateLimit-Remaining"] == "9"

        # Flush Redis before finishing the test
        redis_client.flushdb()
