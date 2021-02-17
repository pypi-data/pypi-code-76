class TinkoffApiError(Exception):
    pass


class TinkoffNetworkError(TinkoffApiError):
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text

    def __str__(self):
        return f"Server sent response with status_code={self.status_code} and text={self.text}"


class TinkoffResponseError(TinkoffApiError):
    def __init__(self, error_code, message=None, details=None):
        self.error_code = error_code
        self.message = message
        self.details = details

    def __str__(self):
        ret = str(self.error_code)
        if self.message:
            ret += f" {self.message}"
        if self.details:
            ret += f": {self.details}"
        return ret


class TinkoffNotifyValidationError(TinkoffApiError):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg
