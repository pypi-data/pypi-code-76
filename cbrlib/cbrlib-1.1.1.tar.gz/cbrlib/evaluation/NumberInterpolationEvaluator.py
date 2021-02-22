from enum import Enum
from typing import Optional

from cbrlib.evaluation.NumberEvaluator import NumberEvaluator


def calculate_distance(v1: float, v2: float, max_distance: float, cyclic: bool) -> float:
    result = abs(v2 - v1)
    if cyclic and result > max_distance:
        return 2 * max_distance - result
    return result


def calculate_max_distance(v: float, max_distance: float, origin: float, use_origin: bool) -> float:
    if use_origin:
        return abs(v - origin)
    return max_distance


def is_less(v1: float, v2: float, max_distance: float, cyclic: bool) -> bool:
    less = v1 < v2
    if cyclic:
        if less:
            left_distance = v2 - v1
        else:
            left_distance = 2 * max_distance - v1 + v2
        right_distance = 2 * max_distance - left_distance
        return left_distance < right_distance
    return less


def interpolate_polynom(stretched_distance: float, linearity: float) -> float:
    if linearity == 1:
        return 1 - stretched_distance
    elif linearity == 0:
        return 0
    return pow(1 - stretched_distance, 1 / linearity)


def interpolate_root(stretched_distance: float, linearity: float) -> float:
    if linearity == 1:
        return 1 - stretched_distance
    elif linearity == 0:
        return 1
    return pow(1 - stretched_distance, linearity)


def interpolate_sigmoid(stretched_distance: float, linearity: float) -> float:
    if linearity == 1:
        return 1 - stretched_distance
    if stretched_distance < 0.5:
        if linearity == 0:
            return 1
        return 1 - pow(2 * stretched_distance, 1 / linearity) / 2
    if linearity == 0:
        return 0
    return pow(2 - 2 * stretched_distance, 1 / linearity) / 2


class NumberInterpolation(Enum):
    Polynom = 1,
    Sigmoid = 2,
    Root = 3,


class NumberInterpolationMetrics:

    def __init__(self, options: Optional[dict] = None):
        self.cyclic = False
        self.origin = 0.0
        self.use_origin = False

        self.equal_if_less = 0.0
        self.tolerance_if_less = 0.5
        self.linearity_if_less = 1.0

        self.equal_if_more = 0.0
        self.tolerance_if_more = 0.5
        self.linearity_if_more = 1.0
        if options is not None:
            for (k, v) in options.items():
                if hasattr(self, k):
                    self.__setattr__(k, v)

        self.__interpolation_if_less = NumberInterpolation.Polynom
        self.__interpolation_if_more = NumberInterpolation.Polynom

        self.__interpolations = {
            NumberInterpolation.Polynom: interpolate_polynom,
            NumberInterpolation.Sigmoid: interpolate_sigmoid,
            NumberInterpolation.Root: interpolate_root
        }

    def get_interpolation_if_more(self):
        return self.__interpolations[self.__interpolation_if_more]

    def set_interpolation_if_more(self, interpolation: NumberInterpolation):
        self.__interpolation_if_more = interpolation

    def get_interpolation_if_less(self):
        return self.__interpolations[self.__interpolation_if_less]

    def set_interpolation_if_less(self, interpolation: NumberInterpolation):
        self.__interpolation_if_less = interpolation

    def to_serializable(self):
        return {
            'cyclic': self.cyclic,
            'origin': self.origin,
            'useOrigin': self.use_origin,

            'equalIfLess': self.equal_if_less,
            'toleranceIfLess': self.tolerance_if_less,
            'linearityIfLess': self.linearity_if_less,

            'equalIfMore': self.equal_if_more,
            'toleranceIfMore': self.tolerance_if_more,
            'linearityIfMore': self.linearity_if_more,

            'interpolationIfLess': self.__interpolation_if_less.name,
            'interpolationIfMore': self.__interpolation_if_more.name,
        }


class NumberInterpolationEvaluator(NumberEvaluator):

    def __init__(self, name: str, min_: float, max_: float,
                 metrics: Optional[NumberInterpolationMetrics] = NumberInterpolationMetrics()):
        super(NumberInterpolationEvaluator, self).__init__(name)
        if max_ > min_:
            self.__max_distance = max_ - min_
            self.__min = min_
            self.__max = max_
        else:
            self.__max_distance = min_ - max_
            self.__min = max_
            self.__max = min_
        self.__metrics = metrics

    def get_typename(self) -> str:
        return "number-interpolation"

    def calculate_similarity(self, query: float, case: float) -> float:
        distance = calculate_distance(query, case, self.__max_distance, self.__metrics.cyclic)
        max_distance = calculate_max_distance(query, self.__max_distance, self.__metrics.origin,
                                              self.__metrics.use_origin)
        if max_distance == 0:
            return 1
        relative_distance = distance / max_distance
        if relative_distance < 1:
            if is_less(case, query, self.__max_distance, self.__metrics.cyclic):
                equal = self.__metrics.equal_if_less
                tolerance = self.__metrics.tolerance_if_less
                linearity = self.__metrics.linearity_if_less
                interpolation = self.__metrics.get_interpolation_if_less()
            else:
                equal = self.__metrics.equal_if_more
                tolerance = self.__metrics.tolerance_if_more
                linearity = self.__metrics.linearity_if_more
                interpolation = self.__metrics.get_interpolation_if_more()
            if relative_distance <= equal:
                return 1
            elif relative_distance >= tolerance:
                return 0
            else:
                stretched_distance = (relative_distance - equal) / (tolerance - equal)
                return interpolation(stretched_distance, linearity)
        return 0

    def to_serializable(self) -> dict:
        result = super(NumberInterpolationEvaluator, self).to_serializable()
        result['min'] = self.__min
        result['max'] = self.__max
        result['metrics'] = self.__metrics.to_serializable()
        return result
