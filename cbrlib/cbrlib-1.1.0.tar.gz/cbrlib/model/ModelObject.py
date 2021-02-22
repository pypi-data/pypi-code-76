from abc import ABC
from typing import Union

from cbrlib.model.ModelElement import ModelElement


class ModelObject(ModelElement, ABC):

    def __init__(self, value):
        super(ModelObject, self).__init__(value)

    def __hash__(self):
        return self.get_value().__hash__()

    def __str__(self):
        return str(self.get_value())

    def __repr__(self):
        return str(self.get_value())

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise ValueError('Lower than comparison must have the same type.')
        return self.get_value() < other.get_value()

    def __gt__(self, other):
        if not isinstance(other, self.__class__):
            raise ValueError('Greater than comparison must have the same type.')
        return self.get_value() > other.get_value()

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, self.__class__):
            raise ValueError('Equal comparison must have the same type.', str(self.__class__), '!=', str(other.__class__))
        return self.get_value() == other.get_value()

    def get_value(self):
        return self.get_id()

    def to_serializable(self) -> Union[dict, list]:
        return self.get_value()
