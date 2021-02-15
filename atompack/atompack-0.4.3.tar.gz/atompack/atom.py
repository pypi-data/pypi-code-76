"""A dict-like abstraction for individual atoms."""

from collections.abc import MutableMapping

import numpy as np
import orjson


class Atom(MutableMapping):
    """Dict like object containing arbitrary atomic properties.

    Note:
        End users should not construct Atom objects directly.
    
    Args:
        specie: Atomic specie.
        position: 3D position in cartesian space.
    """

    def __init__(self, specie: str, position: np.ndarray, **kwargs) -> None:
        self._attrs = {k: v for k, v in kwargs.items()}
        self._attrs["specie"] = specie
        self._attrs["position"] = position

    ######################
    #    Constructors    #
    ######################

    @classmethod
    def from_json(cls, s: str) -> 'Atom':
        """Initializes from a JSON string."""
        # load dict from JSON string
        data = orjson.loads(s)

        # validate type
        _type = data.pop("type")
        if _type != cls.__name__:
            raise TypeError(f"cannot deserialize from type `{_type}`")

        # process specie
        specie = data.pop("specie")
        if specie is None:
            raise ValueError("`specie` is a required attribute")

        # process position
        position = data.pop("position")
        if position is None:
            raise ValueError("`position` is a required attribute")
        position = np.array(position)

        # return instance
        return cls(specie, position, **data)

    #######################################
    #    MutableMapping Implementation    #
    #######################################

    def __getitem__(self, key):
        return self._attrs[key]

    def __setitem__(self, key, value):
        self._attrs[key] = value

    def __delitem__(self, key):
        del self._attrs[key]

    def __iter__(self):
        return iter(self._attrs)

    def __len__(self):
        return len(self._attrs)

    ####################
    #    Properties    #
    ####################

    @property
    def specie(self) -> str:
        """Returns the atomic specie."""
        return self._attrs["specie"]

    @specie.setter
    def specie(self, value: str) -> None:
        self._attrs["specie"] = value

    @property
    def position(self) -> np.ndarray:
        """Returns the atom's position."""
        return self._attrs["position"]

    @position.setter
    def position(self, value: np.ndarray) -> None:
        self._attrs["position"] = value

    ########################
    #    Public Methods    #
    ########################

    def to_json(self) -> str:
        """Returns the JSON serialized representation."""
        _attrs = self._attrs.copy()
        _attrs["type"] = type(self).__name__
        return orjson.dumps(_attrs, option=orjson.OPT_SERIALIZE_NUMPY)
