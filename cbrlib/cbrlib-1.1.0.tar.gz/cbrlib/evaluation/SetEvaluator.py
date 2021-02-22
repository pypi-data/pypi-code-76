from enum import Enum
from functools import reduce
from typing import Optional

from cbrlib.evaluation.SimilarityEvaluator import SimilarityEvaluator
from cbrlib.model.ModelObject import ModelObject
from cbrlib.model.SetObject import SetObject


class SetEvaluationMode(Enum):
    QueryInclusion = 1,
    CaseInclusion = 2,
    Intermediate = 3,


def contains(source: set[ModelObject], value: ModelObject, evaluator: SimilarityEvaluator):
    count = 0
    similarity_sum = 0
    for element in source:
        similarity = evaluator.evaluate(value, element)
        if similarity == 1:
            return 1
        similarity_sum = similarity_sum + similarity
        count = count + 1
    if count == 0:
        return 0
    return float(similarity_sum) / count


def check_inclusion(query: set[ModelObject], case: set[ModelObject], evaluator: SimilarityEvaluator) -> float:
    size_of_query = len(query)
    if size_of_query == 0:
        return 0
    current = reduce(lambda e1, e2: e1 + contains(case, e2, evaluator), [0, *query])
    return float(current) / size_of_query


class SetEvaluator(SimilarityEvaluator):

    def __init__(self, name: str, mode: SetEvaluationMode,
                 element_evaluator: Optional[SimilarityEvaluator] = SimilarityEvaluator.default_evaluator()):
        super(SetEvaluator, self).__init__(name, )
        self.evaluate = {
            1: self.query_inclusion,
            2: self.case_inclusion,
            3: self.intermediate
        }[mode.value[0]]
        self.__mode = mode
        self.__element_evaluator = element_evaluator

    def get_typename(self) -> str:
        return 'set'

    def evaluate(self, query: ModelObject, case: ModelObject) -> float:
        raise NotImplemented()

    def query_inclusion(self, query: SetObject, case: SetObject) -> float:
        return check_inclusion(query.get_value(), case.get_value(), self.__element_evaluator)

    def case_inclusion(self, query: SetObject, case: SetObject) -> float:
        return check_inclusion(case.get_value(), query.get_value(), self.__element_evaluator)

    def intermediate(self, query: SetObject, case: SetObject) -> float:
        a = check_inclusion(query.get_value(), case.get_value(), self.__element_evaluator)
        b = check_inclusion(case.get_value(), query.get_value(), self.__element_evaluator)
        return float(a + b) / 2

    def to_serializable(self) -> dict:
        result = super(SetEvaluator, self).to_serializable()
        result['mode'] = self.__mode.name
        result['elementEvaluator'] = self.__element_evaluator.get_typename()
        return result
