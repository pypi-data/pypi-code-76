"""Declares exceptions used by the FastAPI RESt Framework."""
from fastapi import HTTPException
from unimatrix.ext.model.exc import CanonicalException


class MethodNotAllowed(HTTPException):
    """Raises to indicate that an unsupported HTTP method is requested."""
    status_code = 415
    default_detail = 'Method "{method}" not allowed.'
    default_code = 'method_not_allowed'

    def __init__(self, method, detail=None, code=None):
        if detail is None:
            detail = self.default_detail.format(method=method)
        super().__init__(status_code=self.status_code, detail=detail)


class InvalidAuthorizationScheme(CanonicalException):
    code = 'HTTP_AUTHORIZATION_SCHEME_INVALID'
    http_status_code = 403

    def __init__(self, scheme, supported):
        message = "The Authorization header specified an unknown scheme."
        detail = f"The scheme '{scheme}' is not supported by the server."
        hint = (
            "Use one of the following schemes: "
            f"{str.join(', ', supported)}"
        )
        super().__init__(message=message, hint=hint, detail=detail)


class BearerTokenMissing(CanonicalException):
    code = 'BEARER_TOKEN_MISSING'
    http_status_code = 401


class BearerTokenUnverifiable(CanonicalException):
    code = 'BEARER_TOKEN_UNVERIFIABLE'
    http_status_code = 403
    message = (
        "The authenticity and integrity of the Bearer token could "
        "not be verified."
    )
    detail = (
        "The digital signature included in the Bearer token did "
        "not validate against any trusted key."
    )
