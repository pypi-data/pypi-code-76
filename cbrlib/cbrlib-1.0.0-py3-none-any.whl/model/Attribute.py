from cbrlib.model.ModelClass import ModelClass
from cbrlib.model.ModelElement import ModelElement


class Attribute(ModelElement):

    def __init__(self, id_, model_class: ModelClass):
        super(Attribute, self).__init__(id_)
        self.__model_class = model_class

    def get_model_class(self):
        return self.__model_class

    def to_serializable(self) -> dict:
        result = super(Attribute, self).to_serializable()
        result['class'] = self.__model_class.to_serializable()
        return result
