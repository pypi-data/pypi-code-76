from nidhoggr.errors.common import UnknownError, MethodNotAllowed, NotFound
from nidhoggr.utils.decorator import as_response


@as_response
def not_found(_):
    return NotFound


@as_response
def method_not_allowed(_):
    return MethodNotAllowed


@as_response
def internal_server_error(error):
    return UnknownError.copy(update=dict(cause=f"{error.__class__.__name__}: {error}"))
