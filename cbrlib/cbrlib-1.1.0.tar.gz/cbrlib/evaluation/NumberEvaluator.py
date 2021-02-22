from abc import ABC, abstractmethod

from cbrlib.evaluation.SimilarityEvaluator import SimilarityEvaluator
from cbrlib.model.ModelObject import ModelObject
from cbrlib.model.NumberObject import NumberObject


class NumberEvaluator(SimilarityEvaluator, ABC):

    def __init__(self, name):
        super(NumberEvaluator, self).__init__(name)

    @abstractmethod
    def get_typename(self) -> str:
        return 'number'

    @abstractmethod
    def calculate_similarity(self, query: float, case: float) -> float:
        raise NotImplemented()

    def evaluate(self, query: ModelObject, case: ModelObject) -> float:
        if not isinstance(query, NumberObject) or not isinstance(case, NumberObject):
            return 0
        return self.calculate_similarity(query.to_float(), case.to_float())
