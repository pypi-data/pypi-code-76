from cbrlib.evaluation.SimilarityEvaluator import SimilarityEvaluator
from cbrlib.model.BondObject import BondObject
from cbrlib.model.ModelObject import ModelObject


class LookupTableEvaluator(SimilarityEvaluator):

    def __init__(self, name: str, lookup_table: dict):
        super(LookupTableEvaluator, self).__init__(name)
        self.__lookup_table = lookup_table

    def get_typename(self) -> str:
        return 'lookup'

    def evaluate(self, query: ModelObject, case: ModelObject) -> float:
        query_type = type(query)
        case_type = type(case)
        if not issubclass(query_type, ModelObject) or not issubclass(case_type, ModelObject) or issubclass(
                query_type, BondObject) or issubclass(case_type, BondObject):
            return 0
        similarities = self.__lookup_table.get(query.get_value())
        if similarities is None or case.get_value() not in similarities:
            return super(LookupTableEvaluator, self).evaluate(query, case)
        return similarities.get(case.get_value())

    def to_serializable(self):
        result = super(LookupTableEvaluator, self).to_serializable()
        result['table'] = self.__lookup_table
        return result
