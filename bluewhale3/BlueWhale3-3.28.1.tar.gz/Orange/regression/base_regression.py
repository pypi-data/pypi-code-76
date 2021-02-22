from Orange.base import Learner, Model, SklLearner, SklModel
from Orange.i18n_config import *


def __(key):
    return i18n.t("orange.msg." + key)


__all__ = ["LearnerRegression", "ModelRegression",
           "SklModelRegression", "SklLearnerRegression"]


class LearnerRegression(Learner):
    learner_adequacy_err_msg = __("learner_adequacy_err_msg")

    def check_learner_adequacy(self, domain):
        return domain.has_continuous_class


class ModelRegression(Model):
    pass


class SklModelRegression(SklModel, ModelRegression):
    pass


class SklLearnerRegression(SklLearner, LearnerRegression):
    __returns__ = SklModelRegression
