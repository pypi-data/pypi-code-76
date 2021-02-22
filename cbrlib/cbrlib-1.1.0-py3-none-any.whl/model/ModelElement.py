
from abc import ABC
from typing import final, Union


class ModelElement(ABC):

    def __init__(self, id_):
        self.__id = id_

    def __hash__(self):
        return self.get_id().__hash__

    def __str__(self):
        return str(self.get_id())

    def __repr__(self):
        return str(self.get_id())

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise ValueError('Lower than comparison must have the same type.')
        return self.get_id() < other.get_id()

    def __gt__(self, other):
        if not isinstance(other, self.__class__):
            raise ValueError('Greater than comparison must have the same type.')
        return self.get_id() > other.get_id()

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, self.__class__):
            if other.__class__ is not None:
                raise ValueError('Equal comparison must have the same type.', str(self.__class__), '!=',
                                 str(other.__class__))
            else:
                raise ValueError('Equal comparison must have the same type.', str(self.__class__), '!=',
                                 type(other))
        return self.get_id() == other.get_id()

    @final
    def get_id(self):
        return self.__id

    def set_id(self, id_):
        if self.__id is not None:
            raise ValueError('The id of the model element is already set')
        self.__id = id_

    def to_serializable(self) -> Union[dict, list]:
        return {'id': self.get_id()}
