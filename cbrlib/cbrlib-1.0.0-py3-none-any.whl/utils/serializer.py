from cbrlib.reasoning.ResultListEntry import ResultListEntry
import json
from datetime import datetime, date
from typing import IO, Union, Optional

import yaml

from cbrlib.evaluation.NumberInterpolationEvaluator import NumberInterpolationMetrics
from cbrlib.evaluation.SimilarityEvaluator import SimilarityEvaluator
from cbrlib.model.ModelElement import ModelElement


def json_serializer(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def prepare_serializable(element: Union[ModelElement, list, dict]):
    if isinstance(element, list):
        result = list()
        for e in element:
            result.append(prepare_serializable(e))
    elif isinstance(element, dict):
        result = dict()
        for k, e in element.items():
            result[k] = prepare_serializable(e)
    elif isinstance(element, (ModelElement, SimilarityEvaluator, NumberInterpolationMetrics, ResultListEntry)):
        result = element.to_serializable()
    else:
        result = element
    return result


def to_json_string(element: Union[ModelElement, list, dict]):
    return json.dumps(prepare_serializable(element), default=json_serializer)


def to_json(element: Union[ModelElement, list], fp: IO[str]):
    json.dump(prepare_serializable(element), fp, default=json_serializer)


def to_yaml_string(element: Union[ModelElement, list], is_top: Optional[bool] = True):
    return yaml.dump(prepare_serializable(element))


def to_yaml(element: ModelElement, fp: IO[str],  is_top: Optional[bool] = True):
    yaml.dump(prepare_serializable(element), fp)
