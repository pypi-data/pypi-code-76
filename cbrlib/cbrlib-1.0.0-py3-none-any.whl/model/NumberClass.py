from abc import ABC

from cbrlib.model.ModelClass import ModelClass


class NumberClass(ModelClass, ABC):

    def __init__(self, id_: str):
        super(NumberClass, self).__init__(id_)
