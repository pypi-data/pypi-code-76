from abc import ABC, abstractmethod
from cbrlib.evaluation.SimilarityEvaluator import SimilarityEvaluator
from typing import Iterable, Optional

from cbrlib.evaluation.AssemblyEvaluator import AssemblyEvaluator
from cbrlib.model.AssemblyObject import AssemblyObject
from cbrlib.reasoning.ResultListEntry import ResultListEntry


class InferenceOptions:

    def __init__(self, options: Optional[dict] = None):
        self.skip = 0
        self.limit = 10
        if options is not None:
            for (k, v) in options.items():
                if hasattr(self, k):
                    self.__setattr__(k, v)

class Reasoner(ABC):

    def __init__(self, casebase: Iterable[AssemblyObject], evaluator: AssemblyEvaluator):
        self.__casebase = casebase
        self.__evaluator = evaluator

    def get_casebase(self) -> Iterable[AssemblyObject]:
        return self.__casebase

    def get_evaluator(self):
        return self.__evaluator

    @abstractmethod
    def infer(self, fact: AssemblyObject, options: Optional[InferenceOptions] = InferenceOptions()):
        raise NotImplementedError()