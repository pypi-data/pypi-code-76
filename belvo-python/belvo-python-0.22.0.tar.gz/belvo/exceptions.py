from typing import Any


class BelvoAPIException(Exception):
    ...


class RequestError(BelvoAPIException):
    def __init__(self, status_code: int, detail: Any):
        self.status_code = status_code
        self.detail = detail
