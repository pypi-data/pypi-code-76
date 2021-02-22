from typing import Union

from cbrlib.model.ModelObject import ModelObject
from cbrlib.model.Predicate import Predicate
from cbrlib.model.PredicateError import PredicateError


class RangePredicate(Predicate):

    def __init__(self, min_: ModelObject, max_: ModelObject):
        if min_ < max_:
            self.min = min_
            self.max = max_
        elif max_ > min_:
            self.min = max_
            self.max = min_
        else:
            raise ValueError('min and max has the same value')

    def get_name(self):
        return 'range'

    def read_object(self, value: object) -> ModelObject:
        if value > self.max.get_value():
            raise PredicateError(
                f'The value is greater than {self.max.get_value()}. The allowed range is {self.min.get_value()} <= x <= {self.max.get_value()}')
        if value < self.min.get_value():
            raise PredicateError(f'The value is lower than {self.min.get_value()}.')
        return None

    def to_serializable(self) -> Union[dict, list]:
        result = {'min': self.min.to_serializable(), 'max': self.max.to_serializable()}
        return result
