


# print(attribute_name, f'({query.get_attribute_value(attribute_name)}, {case.get_attribute_value(attribute_name)})', '=',
#       similarity)
#         print('-------')
from cbrlib.evaluation.AssemblyEvaluator import AssemblyEvaluator
from cbrlib.evaluation.SimilarityEvaluator import SimilarityEvaluator
from cbrlib.model.AssemblyObject import AssemblyObject


class AssemblyAverageEvaluator(AssemblyEvaluator):

    def __init__(self, name: str, evaluators: dict):
        super(AssemblyAverageEvaluator, self).__init__(name, evaluators)

    def get_typename(self) -> str:
        return super(AssemblyAverageEvaluator, self).get_typename() + '-average'

    def calculate_similarity(self, query: AssemblyObject, case: AssemblyObject) -> float:
        similarity_sum = 0
        similarity_count = 0
        for attribute_name in query.get_attribute_names():
            weight = self.get_weight(attribute_name, 1)
            attribute_evaluator = self.get_evaluator(attribute_name, SimilarityEvaluator.default_evaluator())
            similarity = attribute_evaluator.evaluate(query.get_attribute_value(attribute_name),
                                                      case.get_attribute_value(attribute_name))
            if weight <= 0:
                continue
            similarity_sum = similarity_sum + (weight * similarity)
            similarity_count = similarity_count + weight
        if similarity_count == 0:
            return 0
        return float(similarity_sum) / similarity_count
