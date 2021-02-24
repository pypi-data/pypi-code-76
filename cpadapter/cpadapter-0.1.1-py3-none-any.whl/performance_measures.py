import numpy as np


def right_guess(y: np.ndarray, 
                preds: np.ndarray) -> float:
     r"""Function used to calculate the coverage of a classification interval

     This function return the fraction of times the confidence interval
     `preds` contains the classes in `y`.

     Parameters
     ----------
     y: numpy.ndarray
          Array of real or predicted classes with length num_samples
     preds: numpy.ndarray
          Array containing the confidence interval predicted for classification cases.
          This type of interval is a boolean matrix with size [num_samples, num_classes],
          where num_classes is the total number of possible classes for the data.
     
     Returns
     -------
     coverage: float
          Fraction of times the classification in `y` are contained in the predicted confidence
          interval.

     Notes
     -----
     This fuction only works with classification cases, where the confidence interval is created
     using the nonconformist package.
     """
     n_samples = len(y)
     count = np.sum(preds[range(len(preds)), y])
     return count/n_samples


def uncertainty(preds: np.ndarray) -> float:
     r"""Function used to calculate the fraction of uncertainty of the predicted confidence interval

     Sometimes the nonconformist inductive conformal predictor returns an interval that contains all
     the possile classes. In these cases no information is provided, thus adding uncertainty to the
     prediction. This function returns the fraction of times the interval created has all the classes.

     Parameters
     ----------
     preds: numpy.ndarray
          The confidence interval, represented by a numpy.ndarray of boolean
          values with size (num_samples, num_classes), where num_classes is the total
          number of classes for the data, and num_samples is the number of samples used
          to create the matrix.

     Returns
     -------
     uncertainty: float
          Number of times the interval created contains all the possible classes.

     Notes
     -----
     This fuction can only be used in confidence interval generated for classification
     cases with the nonconformist package.
     """
     return np.mean(preds.all(axis=1))


def width(preds: np.ndarray) -> float:
     r"""Function that calculates the normalized width of a classification confidence interval

     This measure represents the with of the classification interval `preds`.
     It's calculated as the average number classes in the predicted intervals for
     every sample, dived by the total number of clases.

     Parameters
     ----------
     preds: numpy.ndarray
          The confidence interval, represented by a numpy.ndarray of boolean
     values with size (num_samples, num_classes), where num_classes is the total
     number of classes for the data, and num_samples is the number of samples used
     to create the matrix.

     Returns
     -------
     mean_norm: float
          Normalized width of a classification confidence interval

     Notes
     -----
     This function can only be used in classification confidence intervals created with
     the nonconformist package.
     """
     n_classes = preds.shape[1]
     n_samples = preds.shape[0]
     n_trues = np.sum(preds)
     mean = n_trues / n_samples
     mean_norm = mean / n_classes
     return mean_norm


def picp(real: np.ndarray, lower: np.ndarray, upper: np.ndarray) -> float:
     r"""Function that calculates the coverage of the predicted interval

     The PICP (Prediction Interval Coverage Probability) measures the
     fraction of times the prediction or real data in `real` is above
     the lower bound `lower` and below the upper bound `upper` of the predicted
     confidence interval.

     Parameters
     ----------
     real: numpy.ndarray
          Array of the predicted or real target values.
     lower: numpy.ndarray
          Array of predicted lower bound values.
     upper: numpy.ndarray
          Array of predited upper bound values.

     Returns
     -------
     picp: float
          Fraction of samples that fall inside the predicted interval.

     Notes
     -----
     This measure is useful only for regression confidence intervals created
     with the nonconformist package.

     """
     return ((real <= upper) & (real >= lower)).mean()


def pinaw(real: np.ndarray, lower: np.ndarray, upper: np.ndarray) -> float:
     r"""Function for calulating the normalized average width of a predicted interval

     The PINAW (Prediction Interval Normalized Width) represents the average
     interval width, dived by the range of the data (max value - min value). This 
     fuction calculates de PINAW for a regression interval.

     Parameters
     ----------
     real: numpy.ndarray
          Array of the predicted or real target values.
     lower: numpy.ndarray
          Array of predicted lower bound values.
     upper: numpy.ndarray
          Array of predited upper bound values.

     Returns
     -------
     pinaw: float
          The normalized average width of the predicted interval

     Notes
     -----
     This measure is only useful when the interval is predicted for a
     regression case.
     """
     range = real.max() - real.min()
     width = upper - lower
     return (width.mean()/range)


def relative_width(real: np.ndarray, lower: np.ndarray, upper: np.ndarray) -> float:
     r"""Fuction used fo calculating the average width relative to the value of the target features

     The measure given by this fuction is calculated as the median value of the interval
     width diveded by the target values in `real`.

     Parameters
     ----------
     real: numpy.ndarray
          Array of the predicted or real target values.
     lower: numpy.ndarray
          Array of predicted lower bound values.
     upper: numpy.ndarray
          Array of predited upper bound values.

     Returns
     -------
     median_relative_width: float
          Median value of the width divided by the target feature value.

     Notes
     -----
     This measure is useful for regression cases, not classification.
     """
     width = upper - lower
     return np.median(width/real)


def relative_mean_width(real: np.ndarray, lower: np.ndarray, upper: np.ndarray) -> float:
     r"""Fuction used for calculating the average width relative to the mean value of the target feature.

     The measure returned by this function is calculated as the mean interval width divided by
     the mean target value in `real`.

     Parameters
     ----------
     real: numpy.ndarray
          Array of the predicted or real target values.
     lower: numpy.ndarray
          Array of predicted lower bound values.
     upper: numpy.ndarray
          Array of predited upper bound values.

     Returns
     -------
     relative_mean_width: float
          Average interval width divided by the mean value of the target feature.

     Notes
     -----
     This measure is used for interval created for regression cases
     """
     width = upper - lower
     mean_real = real.mean()
     return width.mean()/mean_real