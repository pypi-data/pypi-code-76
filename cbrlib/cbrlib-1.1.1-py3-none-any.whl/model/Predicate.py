from abc import ABC, abstractmethod
from typing import Union

from cbrlib.model import ModelObject


class Predicate(ABC):

    @abstractmethod
    def get_name(self):
        raise NotImplemented()

    @abstractmethod
    def read_object(self, value: object) -> ModelObject:
        raise NotImplemented()

    @abstractmethod
    def to_serializable(self) -> Union[dict, list]:
        raise NotImplemented()
