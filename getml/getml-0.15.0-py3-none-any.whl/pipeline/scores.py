# Copyright 2021 The SQLNet Company GmbH

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.


"""
Signifies different scoring methods
"""

# --------------------------------------------------------------------
# Scores for classification problems.

auc = "auc"
"""Area under the curve - refers to the area under the receiver
operating characteristic (ROC) curve.

Used for classification problems.

When handling a classification problem, the ROC curve maps the
relationship between two conflicting goals:

On the hand, we want a high *true positive rate*. The true positive
rate, sometimes referred to as *recall*, measures the share of
true positive predictions over all positives:

.. math::

    TPR = \\frac{number \\; of \\; true \\; positives}{number \\; of \\; all \\; positives}

In other words, we want our classification algorithm to "catch" as
many positives as possible.

On the other hand, we also want a low *false positive rate* (FPR). The
false positive rate measures the share of false positives over all
negatives.

.. math::

    FPR = \\frac{number \\; of \\; false \\; positives}{number \\; of \\; all \\; negatives}

In other words, we want as few "false alarms" as possible.

However, unless we have a perfect classifier, these two goals
conflict with each other.

The ROC curve maps the TPR against the FPR. We now measure the area
under said curve (AUC). A higher AUC implies that the trade-off between
TPR and FPR is more benefitial. A perfect model would have an AUC of
1. An AUC of 0.5 implies that the model has no predictive value.

"""

accuracy = "accuracy"
"""Accuracy - measures the share of accurate predictions as of total
samples in the testing set.

Used for classification problems.

.. math::

    accuracy = \\frac{number \\; of \\; correct \\; predictions}{number \\; of \\; all \\; predictions}

The number of correct predictions depends on the threshold used:
For instance, we could interpret all predictions for which the probability
is greater than 0.5 as a positive and all others as a negative.
But we do not have to use a threshold of 0.5 - we might as well
use any other threshold. Which threshold we choose will impact
the calculated accuracy.

When calculating the accuracy, the value returned is the
accuracy returned by the *best threshold*.

Even though accuracy is the most intuitive way to measure a classification
algorithm, it can also be very misleading when the samples are very skewed.
For instance, if only 2% of the samples are positive, a predictor that
always predicts negative outcomes will have an accuracy of 98%. This sounds
very good to the layman, but the predictor in this example
actually has no predictive value.
"""

cross_entropy = "cross_entropy"
"""Cross entropy, also referred to as log-loss, is a measure of the likelihood
of the classification model.

Used for classification problems.

Mathematically speaking, cross-entropy for a binary classification problem
is defined as follows:

.. math::

    cross \\; entropy = - \\frac{1}{N} \\sum_{i}^{N} (y_i \\log p_i + (1 - y_i) \\log(1 - p_i),

where :math:`p_i` is the probability of a positive outcome as predicted
by the classification algorithm and :math:`y_i` is the target value,
which is 1 for a positive outcome and 0 otherwise.

There are several ways to justify the use of cross entropy to evaluate
classification algorithms. But the most intuitive way is to think of
it as a measure of *likelihood*. When we have a classification algorithm
that gives us probabilities, we would like to know how likely it is
that we observe a particular state of the world given the probabilities.

We can calculate this likelihood as follows:

.. math::

    likelihood = \\prod_{i}^{N} (p_i^{y_i} * (1 - p_i)^{1 - y_i}).

(Recall that :math:`y_i` can only be 0 or 1.)

If we take the logarithm of the likelihood as defined above, divide by
:math:`N` and then multiply by `-1` (because we want lower to mean
better and 0 to mean perfect), the outcome will be cross entropy.
"""

# --------------------------------------------------------------------
# Scores for regression problems.

mae = "mae"
"""Mean Absolute Error - measure of distance between two
numerical targets.

Used for regression problems.

.. math::

    MAE = \\frac{\\sum_{i=1}^n | \\mathbf{y}_i - \\mathbf{\\hat{y}}_i |}{n},

where :math:`\\mathbf{y}_i` and :math:`\\mathbf{\\hat{y}}_i` are the target
values or prediction respectively for a particular data sample
:math:`i` (both multidimensional in case of using multiple targets)
while :math:`n` is the number of samples we consider during the
scoring.
"""

rmse = "rmse"
"""Root Mean Squared Error - measure of distance between two
numerical targets.

Used for regression problems.

.. math::

    RMSE = \\sqrt{\\frac{\\sum_{i=1}^n ( \\mathbf{y}_i - \\mathbf{\\hat{y}}_i )^2}{n}},

where :math:`\\mathbf{y}_i` and :math:`\\mathbf{\\hat{y}}_i` are the target
values or prediction respectively for a particular data sample
:math:`i` (both multidimensional in case of using multiple targets)
while :math:`n` is the number of samples we consider during the
scoring.
"""


rsquared = "rsquared"
""":math:`R^{2}` - squared correlation coeefficient between predictions and targets.

Used for regression problems.

:math:`R^{2}` is defined as follows:

.. math::

    R^{2} = \\frac{(\\sum_{i=1}^n ( y_i - \\bar{y_i} ) *  ( \\hat{y_i} - \\bar{\\hat{y_i}} ))^2 }{\\sum_{i=1}^n ( y_i - \\bar{y_i} )^2 \\sum_{i=1}^n ( \\hat{y_i} - \\bar{\\hat{y_i}} )^2 },

where :math:`y_i` are the true values, :math:`\\hat{y_i}` are
the predictions and :math:`\\bar{...}` denotes the mean operator.

An :math:`R^{2}` of 1 implies perfect correlation between the predictions
and the targets and an :math:`R^{2}` of 0 implies no correlation
at all.
"""

# --------------------------------------------------------------------

_all_scores = [accuracy, auc, cross_entropy, mae, rmse, rsquared]

# --------------------------------------------------------------------

_classification_scores = [auc, accuracy, cross_entropy]

# --------------------------------------------------------------------

_minimizing_scores = [cross_entropy, mae, rmse]

# --------------------------------------------------------------------
