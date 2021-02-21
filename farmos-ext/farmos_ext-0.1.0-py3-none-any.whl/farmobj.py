
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, Optional, Type

if TYPE_CHECKING:
    from farmos_ext.farm import Farm  # pylint: disable=cyclic-import


class FarmObj():

    _farm = None

    def __init__(self, farm: Farm, keys: Dict = None):
        self._farm = farm
        self._keys = keys

    @property
    def farm(self):
        return self._farm

    @staticmethod
    def _basic_prop(prop: Any) -> Any:
        """Returns the argument if it is not None."""
        return prop if prop else None

    @staticmethod
    def timestamp_to_datetime(timestamp: int) -> Optional[datetime]:
        """Convert timestampt to datetime or return None."""
        return datetime.fromtimestamp(int(timestamp)) if timestamp else None

    def key(self, key: str) -> Optional[Any]:
        if key in self._keys:
            return self._keys[key]
        else:
            return None

    def attr(self, key: str, ret_type: Type[Any]) -> Type[Any]:
        value = FarmObj._basic_prop(self.key(key))
        return ret_type(value) if value else value

    @property
    def name(self) -> str:
        return self.key('name')
