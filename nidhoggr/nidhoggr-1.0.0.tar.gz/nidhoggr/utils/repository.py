from typing import Union, TypeVar

from nidhoggr.core.response import ErrorResponse
from werkzeug.exceptions import InternalServerError

T = TypeVar("T")


def handle_status(repository_response: Union[ErrorResponse, T]) -> T:
    if isinstance(repository_response, ErrorResponse):
        raise InternalServerError(response=repository_response.reason, description=repository_response.exception)
    return repository_response
