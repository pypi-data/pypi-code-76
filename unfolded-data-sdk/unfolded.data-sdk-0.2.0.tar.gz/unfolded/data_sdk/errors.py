class DataSDKError(Exception):
    """Base exception class."""


class UnknownMediaTypeError(DataSDKError):
    """Unknown Media Type"""


class UnknownDatasetNameError(DataSDKError):
    """Unknown Dataset Name"""


class AuthenticationError(DataSDKError):
    """AuthenticationError"""
