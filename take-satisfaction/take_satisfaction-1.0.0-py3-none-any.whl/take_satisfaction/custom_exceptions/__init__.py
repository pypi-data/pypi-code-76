"""Custom exceptions class for take_satisfaction package.

All classes inherit from `Exception` class.

Classes:
____________
    * InvalidDataframeError
    * AbsentColumnError
    * NoSuitableTranslationError
"""

__all__ = [
    "InvalidDataframeError",
    "AbsentColumnError",
    "NoSuitableTranslationError"
]

from .custom_exceptions import (InvalidDataframeError,
                                AbsentColumnError,
                                NoSuitableTranslationError)
