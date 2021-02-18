"""
All Exceptions thrown
"""


class RestClientException(Exception):
    """
    Base exception, holding the generic error information. Having a base class can make the
    error handling on the caller side easier.
    """
    def __init__(self, status_code=500, message=None):
        self.status_code = status_code
        self.message = message

    def get_status_code(self):
        return self.status_code

    def get_error(self):
        return {
            "status_code": self.status_code,
            "message": self.message
        }


class InvalidServiceResponseException(RestClientException):
    pass


class ValidationErrorException(RestClientException):
    pass


class DuplicateConstraintViolationException(RestClientException):
    pass


class TimeoutException(RestClientException):
    pass


class ConnectionTimeoutException(RestClientException):
    pass


class ReadTimeoutException(RestClientException):
    pass


class ResourceNotFoundException(RestClientException):
    pass


class UnAuthorisedException(RestClientException):
    pass


class ForbiddenException(RestClientException):
    pass


class UnprocessableEntityException(RestClientException):
    pass
