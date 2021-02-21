from cbrlib.model.BondClass import BondClass
from cbrlib.model.ModelClass import ModelClass
from cbrlib.model.ModelObject import ModelObject
from cbrlib.model.SetObject import SetObject


class SetClass(BondClass):

    def __init__(self, id_: str, element_class: ModelClass):
        super(SetClass, self).__init__(id_)
        self.__element_class = element_class

    def get_typename(self) -> str:
        return 'set'

    def create_object(self, value: object) -> ModelObject:
        if not isinstance(value, (set, list, tuple)):
            raise ValueError('Argument must be of type "list".')
        values = set()
        for v in value:
            values.add(self.__element_class.read_object(v))
        return SetObject(values)

    def to_serializable(self):
        result = super(SetClass, self).to_serializable()
        result['elementClass'] = self.__element_class.get_id()
        return result
