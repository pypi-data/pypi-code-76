from abc import ABC
from typing import Iterable, Optional

from cbrlib.evaluation.AssemblyEvaluator import AssemblyEvaluator
from cbrlib.model.AssemblyObject import AssemblyObject
from cbrlib.reasoning.Reasoner import InferenceOptions, Reasoner
from cbrlib.reasoning.ResultListEntry import ResultListEntry


class LinearReasoner(Reasoner):

    def infer(self, fact: AssemblyObject, options: Optional[InferenceOptions] = InferenceOptions()):
        evaluator = self.get_evaluator()
        case_base = self.get_casebase()
        result_list = list()
        for case in case_base:
            similarity = evaluator.evaluate(fact, case)
            result_list.append(ResultListEntry(similarity, case))
        result_list = sorted(result_list, reverse=True)
        start_pos = options.skip
        end_pos = start_pos + options.limit
        return result_list[start_pos:end_pos]
