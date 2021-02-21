from typing import Optional

from pydantic import BaseModel

from nidhoggr.utils.transformer import JSONErrorTransformer


class YggdrasilError(BaseModel, JSONErrorTransformer):
    """Base error class for Yggdrasil-specific errors."""

    status: int
    errorMessage: str
    error: str = "YggdrasilError"
    cause: Optional[str] = None


BadPayload = YggdrasilError(
    status=400,
    errorMessage="Malformed request: incorrect arguments",
)
UnknownError = YggdrasilError(
    status=500,
    errorMessage="Unknown internal error",
)
MethodNotAllowed = YggdrasilError(
    status=405,
    errorMessage=(
        "The method specified in the request is not allowed "
        "for the resource identified by the request URI. "
        "Yggdrasil support only POST requests. "
    ),
)
NotFound = YggdrasilError(
    status=404,
    errorMessage="The server has not found anything matching the request URI",
)
BadRequest = YggdrasilError(
    status=400,
    errorMessage=(
        "The server is refusing to service the request "
        "because the entity of the request is in a format "
        "not supported by the requested resource for the requested method"
    ),
)
