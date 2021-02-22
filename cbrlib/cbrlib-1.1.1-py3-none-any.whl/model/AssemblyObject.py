from cbrlib.model.BondObject import BondObject
from cbrlib.model.ModelObject import ModelObject


class AssemblyObject(BondObject):

    def __init__(self, value: dict[ModelObject]):
        super(AssemblyObject, self).__init__(value)

    def get_attribute_names(self) -> set:
        return set(self.get_value().keys())

    def get_attribute_value(self, name: str):
        return self.get_value().get(name)

    def set_attribute_value(self, name: str, value: ModelObject):
        self.get_value()[name] = value

    def to_serializable(self) -> dict:
        result = dict()
        for k in sorted(self.get_attribute_names()):
            result[k] = self.get_attribute_value(k).to_serializable()
        return result
