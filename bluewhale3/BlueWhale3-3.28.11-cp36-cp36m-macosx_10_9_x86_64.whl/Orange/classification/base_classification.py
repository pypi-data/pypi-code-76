from Orange.base import Learner, Model, SklLearner, SklModel
from Orange.i18n_config import *
def __(key):
    return i18n.t("orange." + key)

__all__ = ["LearnerClassification", "ModelClassification",
           "SklModelClassification", "SklLearnerClassification"]


class LearnerClassification(Learner):
    learner_adequacy_err_msg = __("tip.need_discrete_class_variable")

    def check_learner_adequacy(self, domain):
        return domain.has_discrete_class


class ModelClassification(Model):
    pass


class SklModelClassification(SklModel, ModelClassification):
    pass


class SklLearnerClassification(SklLearner, LearnerClassification):
    __returns__ = SklModelClassification
