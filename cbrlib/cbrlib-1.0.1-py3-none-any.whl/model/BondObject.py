from abc import ABC

from cbrlib.model.ModelObject import ModelObject


class BondObject(ModelObject, ABC):

    def __init__(self, value):
        super(BondObject, self).__init__(value)
