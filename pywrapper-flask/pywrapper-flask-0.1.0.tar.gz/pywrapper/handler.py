from flask import Response


class ErrorHandler:

    def __init__(self):
        pass

    def resolve(self, e) -> Response:
        pass


__handlers = {}


def register_handler(error_filter: ErrorHandler, error_cls):
    __handlers[error_cls] = error_filter


def get_handler(error_cls) -> ErrorHandler:
    return __handlers.get(error_cls)
