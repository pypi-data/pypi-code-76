from typing import final

from cbrlib.model.AssemblyObject import AssemblyObject
from cbrlib.model.Attribute import Attribute
from cbrlib.model.BondClass import BondClass


class AssemblyClass(BondClass):

    def __init__(self, id_: str, attributes: list[Attribute]):
        super(AssemblyClass, self).__init__(id_)
        self.__attributes = dict()
        self.__attribute_list = attributes
        for attribute in attributes:
            self.__attributes[attribute.get_id()] = attribute

    def get_typename(self) -> str:
        return 'assembly'

    @final
    def set_id(self, id_: str):
        super(AssemblyClass, self).set_id(id_)

    def create_object(self, value: object) -> AssemblyObject:
        if not isinstance(value, (list, tuple, dict)):
            raise ValueError('Argument must be of type "tuple" or "dict".')
        if isinstance(value, (list, tuple)):
            return self.__from_list(value)
        return self.__from_list(value.items())

    def read_object(self, value: object) -> AssemblyObject:
        return super(AssemblyClass, self).read_object(value)

    def __from_list(self, value: list):
        assembly = AssemblyObject(dict())
        for (k, v) in value:
            attribute = self.__attributes.get(k)
            if attribute is None:
                raise ValueError(f'The attribute "{k}" is not available for assembly {self.get_id()}.')
            assembly.set_attribute_value(k, attribute.get_model_class().read_object(v))
        return assembly

    def to_serializable(self):
        result = super(AssemblyClass, self).to_serializable()
        result['attributes'] = list(map(lambda a: a.to_serializable(), self.__attributes.values()))
        return result
