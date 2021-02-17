class DataSDKError(Exception):
    """Base exception class."""


class UnknownContentTypeError(DataSDKError):
    """Unknown Content-Type"""
