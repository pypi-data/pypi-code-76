from cbrlib.model.ModelObject import ModelObject


class StringObject(ModelObject):

    def __init__(self, value: str):
        super(StringObject, self).__init__(value)
