import circle


class CircleAPIError(Exception):
    """
    https://developers.circle.com/docs/api-errors
    """

    def __init__(
        self, message=None, body=None, status_code=None, headers=None, code=None
    ):
        self.message = message
        self.body = body
        self.status_code = status_code
        self.headers = headers or {}
        self.code = code
        self.request_id = self.headers.get("X-Request-Id", None)

    def __str__(self):
        msg = self.message
        if self.request_id:
            return f"Request {self.request_id}: {msg}"
        else:
            return msg

    def __repr__(self):
        return f"{self.__class__.__name__}(message={self.message}, status_code={self.status_code}, request_id={self.request_id})"


class AuthenticationError(CircleAPIError):
    pass


# Entity Errors:

# TODO: this might not actually be suited as an exception. Will come back to it.
class CircleEntityErrors(Exception):

    """
    https://developers.circle.com/docs/api-errors
    """

    pass
