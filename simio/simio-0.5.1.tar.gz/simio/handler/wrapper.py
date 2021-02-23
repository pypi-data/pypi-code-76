from functools import wraps
from typing import Callable, Any

from simio.handler.request_validator import AbstractRequestValidator


def wrap_handler(handler: Callable, request_validator: AbstractRequestValidator):
    """
    Decorator that collects data from request and adds them to function kwargs
    """

    @wraps(handler)
    async def wrapper(request, *args, **kwargs) -> Any:
        validated_request_data = await request_validator.validate(request)
        kwargs.update(**validated_request_data)
        return await handler(*args, **kwargs)

    return wrapper
