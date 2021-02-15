from abc import ABC
from copy import deepcopy

__all__ = [
    "BaseConnection"
]


class BaseConnection(ABC):
    """
    Base class for storage Connections.
    """

    def to_dict(self) -> dict:
        """Return a json dictionary representing this model."""
        return vars(self)
