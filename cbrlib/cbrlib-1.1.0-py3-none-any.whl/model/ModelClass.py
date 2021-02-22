from abc import ABC, abstractmethod

from cbrlib.model.ModelElement import ModelElement
from cbrlib.model.ModelObject import ModelObject
from cbrlib.model.Predicate import Predicate


class ModelClass(ModelElement, ABC):

    def __init__(self, id_: str):
        super(ModelClass, self).__init__(id_)
        self.predicate = None

    @abstractmethod
    def get_typename(self) -> str:
        raise NotImplemented()

    @abstractmethod
    def create_object(self, value: object) -> ModelObject:
        raise NotImplemented()

    def read_object(self, value: object) -> ModelObject:
        if self.has_predicate():
            value_object = self.get_predicate().read_object(value)
            if value_object is not None:
                return value_object
        return self.create_object(value)

    def has_predicate(self) -> bool:
        if self.predicate is None:
            return False
        return True

    def get_predicate(self) -> Predicate:
        return self.predicate

    def set_predicate(self, predicate: Predicate):
        self.predicate = predicate

    def to_serializable(self):
        json = super(ModelClass, self).to_serializable()
        json['type'] = self.get_typename()
        if self.has_predicate():
            json[self.get_predicate().get_name()] = self.get_predicate().to_serializable()
        return json
