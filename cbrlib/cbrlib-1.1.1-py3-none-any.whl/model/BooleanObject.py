from cbrlib.model.ModelObject import ModelObject


class BooleanObject(ModelObject):

    def __init__(self, value: bool):
        super(BooleanObject, self).__init__(value)
