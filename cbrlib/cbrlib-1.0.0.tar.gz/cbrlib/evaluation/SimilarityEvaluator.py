from abc import ABC

from cbrlib.model import ModelObject


class SimilarityEvaluator(ABC):

    @staticmethod
    def default_evaluator():
        return default_evaluator

    def __init__(self, name: str):
        self.__name = name

    def evaluate(self, query: ModelObject, case: ModelObject) -> float:
        if query != case:
            return 0
        return 1

    def get_name(self):
        return self.__name

    def get_typename(self) -> str:
        return 'equals'

    def to_serializable(self) -> dict:
        return {'name': self.get_name(), 'type': self.get_typename()}


default_evaluator = SimilarityEvaluator('DefaultEvaluator')
