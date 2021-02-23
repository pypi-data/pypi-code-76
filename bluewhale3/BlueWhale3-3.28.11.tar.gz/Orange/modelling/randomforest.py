from Orange.base import RandomForestModel
from Orange.classification import RandomForestLearner as RFClassification
from Orange.data import Variable
from Orange.modelling import SklFitter
from Orange.preprocess.score import LearnerScorer
from Orange.regression import RandomForestRegressionLearner as RFRegression
from Orange.i18n_config import *
def __(key):
    return i18n.t("orange." + key)

__all__ = ['RandomForestLearner']


class _FeatureScorerMixin(LearnerScorer):
    feature_type = Variable
    class_type = Variable

    def score(self, data):
        model = self.get_learner(data)(data)
        return model.skl_model.feature_importances_, model.domain.attributes


class RandomForestLearner(SklFitter, _FeatureScorerMixin):
    name = __('name.random_forest')

    __fits__ = {'classification': RFClassification,
                'regression': RFRegression}

    __returns__ = RandomForestModel
