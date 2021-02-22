from abc import ABC

from cbrlib.model.ModelClass import ModelClass


class BondClass(ModelClass, ABC):

    def __init__(self, id_):
        super(BondClass, self).__init__(id_)
