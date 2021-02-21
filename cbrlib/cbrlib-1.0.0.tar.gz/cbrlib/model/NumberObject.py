from abc import ABC, abstractmethod

from cbrlib.model.ModelObject import ModelObject


class NumberObject(ModelObject, ABC):

    def __init__(self, value: int):
        super(NumberObject, self).__init__(value)

    @abstractmethod
    def to_float(self):
        raise NotImplemented()