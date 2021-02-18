from enum import Enum


class NotePartType(str, Enum):
    TEXT = "text"
    CODE = "code"
    TABLE = "table"
    LIST_BULLET = "list_bullet"
    LIST_NUMBER = "list_number"
    LIST_CHECKBOX = "list_checkbox"
    EXTERNAL_FILE = "external_file"

    def __str__(self) -> str:
        return str(self.value)
