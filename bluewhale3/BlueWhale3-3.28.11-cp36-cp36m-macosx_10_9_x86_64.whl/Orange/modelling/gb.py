from typing import Tuple

import numpy as np

from Orange.base import SklLearner
from Orange.classification import GBClassifier
from Orange.data import Variable, Table
from Orange.modelling import SklFitter
from Orange.preprocess.score import LearnerScorer
from Orange.regression import GBRegressor
from Orange.i18n_config import *


def __(key):
    return i18n.t("orange." + key)


__all__ = ["GBLearner"]


class _FeatureScorerMixin(LearnerScorer):
    feature_type = Variable
    class_type = Variable

    def score(self, data: Table) -> Tuple[np.ndarray, Tuple[Variable]]:
        model: SklLearner = self.get_learner(data)(data)
        return model.skl_model.feature_importances_, model.domain.attributes


class GBLearner(SklFitter, _FeatureScorerMixin):
    name = __("msg.gradient_boosting") + "(scikit-learn)"
    __fits__ = {"classification": GBClassifier,
                "regression": GBRegressor}
