from werkzeug.exceptions import Forbidden


class RateLimiterException(Exception):
    pass


class RateLimitExceeded(RateLimiterException, Forbidden):
    """Raise if the user has exceeded the rate limit."""

    description = "You have exceeded the rate limit."


class RateLimiterConfigValidationError(RateLimiterException):
    pass
