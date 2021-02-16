import warnings

import numpy as np

from sklearn.exceptions import UndefinedMetricWarning
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import binarize

from behalearn.preprocessing import trapezoid_diagonal_intersection


def tpr_score(y_true, y_pred, zero_division='warn'):
    r"""Compute the true positive rate (TPR):
    
    .. math::
        
        \frac{
            \mathit{true\ positives}}
            {\mathit{true\ positives} + \mathit{false\ negatives}}
    
    The best value is 1 and the worst value is 0.
    
    This function accepts class labels of 0 and 1, representing negative and
    positive classes, respectively. For multiclass data, all labels with value
    above 1 are converted to 1 and values below 0 are converted to 0.
    
    Parameters
    ----------
    y_true : array-like
        Expected target values (ground truth).
    
    y_pred : array-like
        Predicted target values as returned by an estimator.
    
    zero_division : ``'warn'``, 0 or 1
        Value to return if the denominator is 0. If ``'warn'``, 0 is returned
        and a warning is raised.
    
    Returns
    -------
    score : float
        The true positive rate.
    """
    _, _, fn, tp = _get_binary_pred_counts(y_true, y_pred)
    return _handle_score(tp, tp + fn, tpr_score.__name__, zero_division)


def fmr_score(y_true, y_pred, zero_division='warn'):
    r"""Compute the false match rate (FMR):
    
    .. math::
    
        \frac{
            \mathit{false\ positives}}
            {\mathit{false\ positives} + \mathit{true\ negatives}}
    
    The best value is 0 and the worst value is 1.
    
    This function accepts class labels of 0 and 1, representing negative and
    positive classes, respectively. For multiclass data, all labels with value
    above 1 are converted to 1 and values below 0 are converted to 0.
    
    Parameters
    ----------
    y_true : array-like
        Expected target values (ground truth).
    
    y_pred : array-like
        Predicted target values as returned by an estimator.
    
    zero_division : ``'warn'``, 0 or 1
        Value to return if the denominator is 0. If ``'warn'``, 0 is returned
        and a warning is raised.
    
    Returns
    -------
    score : float
        The false match rate.
    """
    tn, fp, _, _ = _get_binary_pred_counts(y_true, y_pred)
    return _handle_score(fp, fp + tn, tpr_score.__name__, zero_division)


def fnmr_score(y_true, y_pred, zero_division='warn'):
    r"""Compute the false non-match rate (FNMR):
    
    .. math::
    
        \frac{
            \mathit{false\ negatives}}
            {\mathit{true\ positives} + \mathit{false\ negatives}}
    
    The best value is 0 and the worst value is 1.
    
    This function accepts class labels of 0 and 1, representing negative and
    positive classes, respectively. For multiclass data, all labels with value
    above 1 are converted to 1 and values below 0 are converted to 0.
    
    Parameters
    ----------
    y_true : array-like
        Expected target values (ground truth).
    
    y_pred : array-like
        Predicted target values as returned by an estimator.
    
    zero_division : ``'warn'``, 0 or 1
        Value to return if the denominator is 0. If ``'warn'``, 0 is returned
        and a warning is raised.
    
    Returns
    -------
    score : float
        The false non-match rate.
    """
    _, _, fn, tp = _get_binary_pred_counts(y_true, y_pred)
    return _handle_score(fn, tp + fn, tpr_score.__name__, zero_division)


def hter_score(y_true, y_pred, zero_division='warn'):
    r"""Compute the half-total error rate (HTER):
    
    .. math::
    
        \frac{\mathit{FMR} + \mathit{FNMR}}{2}
    
    The best value is 0 and the worst value is 1.
    
    This function accepts class labels of 0 and 1, representing negative and
    positive classes, respectively. For multiclass data, all labels with value
    above 1 are converted to 1 and values below 0 are converted to 0.
    
    Parameters
    ----------
    y_true : array-like
        Expected target values (ground truth).
    
    y_pred : array-like
        Predicted target values as returned by an estimator.
    
    zero_division : ``'warn'``, 0 or 1
        Value to return if the denominator is 0. If ``'warn'``, 0 is returned
        and a warning is raised.
    
    Returns
    -------
    score : float
        The half-total error rate.
    
    See Also
    --------
    fmr_score, fnmr_score
    """
    fmr = fmr_score(y_true, y_pred, zero_division=zero_division)
    fnmr = fnmr_score(y_true, y_pred, zero_division=zero_division)

    return (fmr + fnmr) / 2


def _get_binary_pred_counts(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    if y_true.size == 0 or y_pred.size == 0:
        return [0] * 4

    binary_y_true = binarize([y_true]).flatten()
    binary_y_pred = binarize([y_pred]).flatten()

    pred_counts = confusion_matrix(binary_y_true, binary_y_pred).ravel()

    if pred_counts.shape[0] == 1:
        if y_true[0] == 1:
            return 0, 0, 0, pred_counts[0]
        else:
            return pred_counts[0], 0, 0, 0
    else:
        return pred_counts


def _handle_score(
        numerator, denominator, function_name, zero_division):
    if denominator != 0:
        return numerator / denominator
    else:
        if zero_division == 'warn':
            replacement_value = 0
            warnings.warn(
                (f'Zero division occurred in "{function_name}".'
                 f' Returning {replacement_value} instead.'),
                UndefinedMetricWarning)
        else:
            replacement_value = int(bool(zero_division))

        return replacement_value


def eer_score(thresholds, fmrs, fnmrs):
    """Compute the equal error rate (EER) and its corresponding threshold
    value.
    
    The EER is the point (threshold value) at which the false match rate (FMR)
    equals the false non-match rate (FNMR).
    
    If there is no exact threshold value in ``thresholds`` at which FMR = FNMR,
    the EER is interpolated from two adjacent pairs of FMR and FNMR values for
    which the inequality between FMR and FNMR changes.
    
    Parameters
    ----------
    thresholds : array-like
        Threshold values (prediction scores).
    
    fmrs : array-like
        FMR values corresponding to the ``thresholds``.
    
    fnmrs : array-like
        FNMR values corresponding to the ``thresholds``.
    
    Returns
    -------
    result : tuple (float, float)
        A tuple of (threshold, EER). If the EER could not be not found,
        ``(numpy.nan, numpy.nan)`` is returned.

    See Also
    --------
    trapezoid_diagonal_intersection
        Used by this function to calculate an approximation of the EER if no
        exact threshold is found in ``thresholds``.
    """
    for i in range(len(fmrs)):
        if fmrs[i] == fnmrs[i]:
            return thresholds[i], fmrs[i]
        if fnmrs[i] > fmrs[i]:
            if i > 0:
                return trapezoid_diagonal_intersection(
                    (thresholds[i], fmrs[i]),
                    (thresholds[i], fnmrs[i]),
                    (thresholds[i - 1], fmrs[i - 1]),
                    (thresholds[i - 1], fnmrs[i - 1]))
            else:
                return thresholds[i], (fmrs[i] + fnmrs[i]) / 2

    return (np.nan, np.nan)
