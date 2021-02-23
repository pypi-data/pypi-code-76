from Orange.classification import SklTreeLearner
from Orange.classification import TreeLearner as ClassificationTreeLearner
from Orange.modelling import Fitter, SklFitter
from Orange.regression import TreeLearner as RegressionTreeLearner
from Orange.regression.tree import SklTreeRegressionLearner
from Orange.tree import TreeModel
from Orange.i18n_config import *
def __(key):
    return i18n.t("orange." + key)

__all__ = ['SklTreeLearner', 'TreeLearner']


class SklTreeLearner(SklFitter):
    name = __('name.tree')

    __fits__ = {'classification': SklTreeLearner,
                'regression': SklTreeRegressionLearner}


class TreeLearner(Fitter):
    name = __('name.tree')

    __fits__ = {'classification': ClassificationTreeLearner,
                'regression': RegressionTreeLearner}

    __returns__ = TreeModel
