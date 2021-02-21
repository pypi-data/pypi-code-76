from cbrlib.model.NumberObject import NumberObject


class IntegerObject(NumberObject):

    def __init__(self, value: int):
        super(IntegerObject, self).__init__(value)

    def to_float(self):
        return float(self.get_value())
