from abc import ABC


class TeralityError(Exception, ABC):
    """Base class for all Terality errors"""
    pass


class PandasError(TeralityError):
    pass


class TeralityValueError(TeralityError):
    pass


class TeralityKeyError(TeralityError):
    pass


class TeralityTypeError(TeralityError):
    pass


class TeralityNotImplementedError(TeralityError):
    pass


class TeralityAuthError(TeralityError):
    pass


class TeralityNetworkError(TeralityError):
    pass


class TeralityInternalError(TeralityError):
    pass


class TeralityDataUploadError(TeralityError):
    pass


class TeralityDataDownloadError(TeralityError):
    pass


class TeralityNotFoundError(TeralityError):
    pass


class TeralityExpiredError(TeralityError):
    pass


_error_mapping = {
    'value': TeralityValueError,
    'key': TeralityKeyError,
    'type': TeralityTypeError,
    'not_implemented': TeralityNotImplementedError,
    'pandas': PandasError,
    'auth': TeralityAuthError,
    'not_found': TeralityNotFoundError,
    'expired': TeralityExpiredError,
}
