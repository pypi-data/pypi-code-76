
from cbrlib.model.BooleanObject import BooleanObject
from cbrlib.model.ModelClass import ModelClass
from cbrlib.model.ModelObject import ModelObject


class BooleanClass(ModelClass):
    TrueObject = BooleanObject(True)
    FalseObject = BooleanObject(False)

    def __init__(self, id_: str):
        super(BooleanClass, self).__init__(id_)

    def get_typename(self) -> str:
        return 'boolean'

    def create_object(self, value: object) -> ModelObject:
        if isinstance(value, str):
            if value.lower() == "true":
                return BooleanClass.TrueObject
            return BooleanClass.FalseObject
        if isinstance(value, (int, float)):
            if value == 0:
                return BooleanClass.FalseObject
            return BooleanClass.TrueObject
        if isinstance(value, bool):
            if value is False:
                return BooleanClass.FalseObject
            return BooleanClass.TrueObject
        if value is not None:
            return BooleanClass.TrueObject
        return BooleanClass.FalseObject
