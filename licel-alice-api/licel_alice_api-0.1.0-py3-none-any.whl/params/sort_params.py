from enum import Enum


class SortDirection(Enum):
    ASC = "asc"
    DESC = "desc"

    def __str__(self) -> str:
        return str(self.value)


class SortParams:
    """
    List sort parameters
    """

    field: str
    direction: SortDirection

    def __init__(self, field: str, direction: SortDirection = SortDirection.ASC):
        """
        :param field: field name for sort
        :param direction: sort direction `asc` or `desc`
        """
        self.field = field
        self.direction = direction

    def __str__(self) -> str:
        return f"{self.field},{self.direction}"
