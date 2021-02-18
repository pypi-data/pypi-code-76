from enum import Enum


class AssayRunCreateValidationStatus(str, Enum):
    VALID = "VALID"
    INVALID = "INVALID"

    def __str__(self) -> str:
        return str(self.value)
