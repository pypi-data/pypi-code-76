from math import sqrt

from cbrlib.evaluation.AssemblyEvaluator import AssemblyEvaluator
from cbrlib.model.AssemblyObject import AssemblyObject


class AssemblyEuclideanEvaluator(AssemblyEvaluator):

    def __init__(self, name: str, evaluators: dict):
        super(AssemblyEuclideanEvaluator, self).__init__(name, evaluators)

    def get_typename(self) -> str:
        return 'assembly-euclidean'

    def calculate_similarity(self, query: AssemblyObject, case: AssemblyObject) -> float:
        similarity_sum = 0
        for attribute_name in query.get_attribute_names():
            attribute_evaluator = self.get_evaluator(attribute_name)
            if attribute_evaluator is None:
                continue
            similarity = attribute_evaluator.evaluate(query.get_attribute_value(attribute_name),
                                                      case.get_attribute_value(attribute_name))
            if similarity <= 0:
                continue
            similarity_sum = float(similarity_sum) + (float(similarity) ** 2)
        return sqrt(similarity_sum)
