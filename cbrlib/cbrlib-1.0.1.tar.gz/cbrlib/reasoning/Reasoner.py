from abc import ABC
from typing import Iterable

from cbrlib.evaluation.AssemblyEvaluator import AssemblyEvaluator
from cbrlib.model.AssemblyObject import AssemblyObject
from cbrlib.reasoning.ResultListEntry import ResultListEntry


class Reasoner(ABC):

    def __init__(self, name: str, case_base: Iterable[AssemblyObject], default_evaluator: AssemblyEvaluator):
        self.__name = name
        self.__case_base = case_base
        self.__default_evaluator = default_evaluator

    def get_name(self):
        return self.__name

    def infer(self, fact: AssemblyObject):
        evaluator = self.__default_evaluator
        case_base = self.__case_base
        result_list = list()
        for case in case_base:
            similarity = evaluator.evaluate(fact, case)
            result_list.append(ResultListEntry(similarity, case))
        result_list = sorted(result_list, reverse=True)
        return result_list[:3]
