from typing import Union

from cbrlib.model.BondObject import BondObject
from cbrlib.model.ModelObject import ModelObject


class SetObject(BondObject):

    def __init__(self, value: set[ModelObject]):
        super(SetObject, self).__init__(value)

    def add_element(self, element: ModelObject):
        self.get_value().add(element)

    def remove_element(self, element: ModelObject):
        self.get_value().remove(element)

    def to_serializable(self) -> Union[dict, list]:
        return list(map(lambda e: e.to_serializable(), self.get_value()))
