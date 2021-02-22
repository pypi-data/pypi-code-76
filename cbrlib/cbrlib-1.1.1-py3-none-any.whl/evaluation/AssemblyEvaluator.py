from abc import abstractmethod, ABC
from typing import Optional

from cbrlib.evaluation.SimilarityEvaluator import SimilarityEvaluator
from cbrlib.model.AssemblyObject import AssemblyObject
from cbrlib.model.ModelObject import ModelObject
from cbrlib.utils.serializer import prepare_serializable


class AssemblyEvaluator(SimilarityEvaluator, ABC):

    def __init__(self, name: str, evaluators: dict):
        super(AssemblyEvaluator, self).__init__(name)
        self.__evaluators = evaluators

    @abstractmethod
    def get_typename(self) -> str:
        return 'assembly'

    def evaluate(self, query: ModelObject, case: ModelObject) -> float:
        if not isinstance(query, AssemblyObject) or not isinstance(case, AssemblyObject):
            return 0
        return float(self.calculate_similarity(query, case))

    def get_weight(self, attribute_name: str, default_weight: Optional[float] = 0) -> float:
        bucket = self.__evaluators.get(attribute_name)
        if bucket is None or 'weight' not in bucket:
            return default_weight
        return bucket['weight']

    def get_evaluator(self, attribute_name: str, default_evaluator: Optional[SimilarityEvaluator] = None) -> float:
        bucket = self.__evaluators.get(attribute_name)
        if bucket is None or 'evaluator' not in bucket:
            return default_evaluator
        return bucket['evaluator']

    @abstractmethod
    def calculate_similarity(self, query: AssemblyObject, case: AssemblyObject) -> float:
        raise NotImplemented()

    def to_serializable(self) -> dict:
        result = super(AssemblyEvaluator, self).to_serializable()
        result['evaluators'] = prepare_serializable(self.__evaluators)
        return result
