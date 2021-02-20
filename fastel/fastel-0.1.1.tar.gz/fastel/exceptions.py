from typing import Any


class APIException(Exception):
    def __init__(self, status_code: int, error: str, detail: Any):
        super().__init__(detail)
        self.status_code = status_code
        self.error = error
        self.detail = detail
