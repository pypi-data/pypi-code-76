from cbrlib.model.NumberObject import NumberObject


class FloatObject(NumberObject):

    def __init__(self, id_):
        super(FloatObject, self).__init__(id_)

    def to_float(self):
        return self.get_value()
