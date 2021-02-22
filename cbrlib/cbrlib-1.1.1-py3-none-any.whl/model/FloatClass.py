from cbrlib.model.FloatObject import FloatObject
from cbrlib.model.ModelObject import ModelObject
from cbrlib.model.NumberClass import NumberClass


class FloatClass(NumberClass):

    def __init__(self, id_: str):
        super(FloatClass, self).__init__(id_)

    def get_typename(self) -> str:
        return 'float'

    def create_object(self, value: object) -> ModelObject:
        if isinstance(value, (str, int)):
            return FloatObject(float(value))
        if not isinstance(value, float):
            raise ValueError('Argument must be of type "float".')
        return FloatObject(value)
