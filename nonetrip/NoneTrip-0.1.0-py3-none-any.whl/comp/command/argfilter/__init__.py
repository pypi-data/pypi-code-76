from typing import Optional

from nonetrip.comp.typing import Message_T


class ValidateError(ValueError):
    def __init__(self, message: Optional[Message_T] = None):
        self.message = message


__all__ = [
    "ValidateError",
]
