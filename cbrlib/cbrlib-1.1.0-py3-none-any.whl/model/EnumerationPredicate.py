from typing import Union, Iterable

from cbrlib.model.ModelObject import ModelObject
from cbrlib.model.Predicate import Predicate
from cbrlib.model.PredicateError import PredicateError


class EnumerationPredicate(Predicate):

    def __init__(self, value_range: Iterable[ModelObject]):
        super(EnumerationPredicate, self).__init__()
        self.value_range = dict()
        for value_object in value_range:
            if not isinstance(value_object, ModelObject):
                raise ValueError('List entry must be of type "ModelObject".')
            self.value_range[value_object.get_id()] = value_object

    def get_name(self):
        return 'enumeration'

    def read_object(self, value: object) -> ModelObject:
        value_object = self.value_range.get(value)
        if value_object is None:
            raise PredicateError('The value is not included in the enumeration.')
        return value_object

    def to_serializable(self) -> Union[dict, list]:
        json = list(map(lambda vo: vo.to_serializable(), sorted(self.value_range.values())))
        return json
