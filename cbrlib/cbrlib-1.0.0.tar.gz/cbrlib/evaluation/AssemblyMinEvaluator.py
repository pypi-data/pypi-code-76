from cbrlib.evaluation.AssemblyEvaluator import AssemblyEvaluator
from cbrlib.evaluation.SimilarityEvaluator import SimilarityEvaluator
from cbrlib.model.AssemblyObject import AssemblyObject


class AssemblyMinEvaluator(AssemblyEvaluator):

    def __init__(self, name: str, evaluators: dict):
        super(AssemblyMinEvaluator, self).__init__(name, evaluators)

    def get_typename(self) -> str:
        return 'assembly-min'

    def calculate_similarity(self, query: AssemblyObject, case: AssemblyObject) -> float:
        similarity_result = 1
        for attribute_name in query.get_attribute_names():
            attribute_evaluator = self.get_evaluator(attribute_name, SimilarityEvaluator.default_evaluator())
            similarity = attribute_evaluator.evaluate(query.get_attribute_value(attribute_name),
                                                      case.get_attribute_value(attribute_name))
            if similarity <= 0:
                continue
            similarity_result = min(similarity_result, similarity)
        return float(similarity_result)
